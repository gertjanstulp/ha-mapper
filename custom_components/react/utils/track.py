

from typing import Generic, Type, TypeVar, Union

from anyio import Any
from homeassistant.const import ATTR_ID
from homeassistant.core import Event, callback
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import TrackTemplate, TrackTemplateResult, async_track_template_result
from homeassistant.helpers.template import Template, is_template_string

from .updatable import Updatable, callable_type
from ..base import ReactBase
from ..utils.context import TemplateContext
from ..utils.struct import DynamicData, MultiItem
from ..utils.updatable import Updatable

from ..const import (
    PROP_ATTR_TYPE_POSTFIX,
    PROP_TYPE_DEFAULT,
    PROP_TYPE_SOURCE,
    PROP_TYPE_TEMPLATE,
    PROP_TYPE_VALUE,
    SIGNAL_TRACK_UPDATE
)

T = TypeVar('T', bound=DynamicData)


class BaseTracker(Updatable):

    def __init__(self, react: ReactBase) -> None:
        super().__init__(react)
        self.react = react


    def start(self):
        pass


    @callback
    def async_refresh(self):
        pass


class CompositeTracker(BaseTracker, Generic[T]):
    def __init__(self, react: ReactBase, config_source: DynamicData, tctx: TemplateContext, t_type: Type[T] = DynamicData) -> None:
        super().__init__(react)

        self.config_source = config_source
        self.names = config_source.names
        self.tctx = tctx

        self.trackers: list[BaseTracker] = []
        self.value_container = t_type()
        if id := self.config_source.get(ATTR_ID):
            self.value_container.set(ATTR_ID, id)

        for attr in config_source.names:
            self.add_tracker(attr, PROP_TYPE_SOURCE)

        self.start()


    def as_trace_dict(self) -> dict:
        return { name : self.value_container.get(name) for name in self.config_source.names }
    

    def is_template(self, attr: str) -> bool:
        type_prop = f"_{attr}{PROP_ATTR_TYPE_POSTFIX}"
        return getattr(self, type_prop, PROP_TYPE_DEFAULT) == PROP_TYPE_TEMPLATE


    def add_tracker(self, attr: str, type_converter: Any, default: Any = None) -> None:
        attr_value = getattr(self.config_source, attr, None)
        
        def set_attr(attr: str, value: Any, prop_type: str):
            self.set_property(attr, value)
            self.set_property_type(attr, prop_type)

        if isinstance(attr_value, MultiItem):
            tracker = MultiItemTracker(self.react, attr_value, self.tctx)
            self.set_property(attr, tracker.value_container)
            self.trackers.append(tracker)
        elif isinstance(attr_value, DynamicData):
            tracker = ObjectTracker(self.react, attr_value, self.tctx)
            self.set_property(attr, tracker.value_container)
            self.trackers.append(tracker)
        elif isinstance(attr_value, list):
            if len(attr_value) > 0 and isinstance(attr_value[0], DynamicData):
                trackers = [ ObjectTracker(self.react, item, self.tctx) for item in attr_value]
                self.set_property(attr, [ tracker.value_container for tracker in trackers ])
            else:
                pass
        elif attr_value:
            if isinstance(attr_value, str) and is_template_string(attr_value):
                set_attr(attr, None, PROP_TYPE_TEMPLATE)
                self.trackers.append(TemplatePropertyTracker(self.react, self, attr, Template(attr_value), type_converter, self.tctx, self.async_update))
            else:
                set_attr(attr, attr_value, PROP_TYPE_VALUE)
        else:
            set_attr(attr, default, PROP_TYPE_DEFAULT)


    def set_property(self, attr: str, value: Any):
        if hasattr(self.value_container, attr) and getattr(self.value_container, attr) == value: 
            return
        self.value_container.set(attr, value)
        async_dispatcher_send(self.react.hass, SIGNAL_TRACK_UPDATE, self.value_container, attr)


    def set_property_type(self, attr: str, prop_type: str):
        type_prop = f"_{attr}{PROP_ATTR_TYPE_POSTFIX}"
        setattr(self, type_prop, prop_type)


    def start(self):
        if self.tctx:
            @callback
            def async_update_template_trackers():
                for tracker in self.trackers:
                    tracker.async_refresh()
            self.tctx.on_update(async_update_template_trackers)
        
        for tracker in self.trackers:
            tracker.start()


    def destroy(self) -> None:
        super().destroy()
        for tracker in self.trackers:
            tracker.destroy()


class MultiItemTracker(CompositeTracker[MultiItem]):

    def __init__(self, react: ReactBase, config_source: MultiItem, tctx: TemplateContext) -> None:
        super().__init__(react, config_source, tctx, MultiItem)


class ObjectTracker(CompositeTracker[T], Generic[T]):

    def __init__(self, react: ReactBase, config_source: DynamicData, tctx: TemplateContext, t_type: Type[T] = DynamicData) -> None:
        super().__init__(react, config_source, tctx, t_type)


class TemplatePropertyTracker(BaseTracker):
    
    def __init__(self, react: ReactBase, owner: CompositeTracker, property: str, template: Template, type_converter: Any, tctx: TemplateContext, update_callback: callable_type = None):
        super().__init__(react)
        self.react = react
        self.owner = owner
        self.property = property
        self.template = template
        self.type_converter = type_converter
        self.tctx = tctx

        self.runtime_variables: dict = None

        template.hass = react.hass
        if update_callback:
            self.on_update(update_callback)


    def start(self):
        self.owner.set_property(self.property, None)
        self.runtime_variables = {}
        self.tctx.build(self.runtime_variables)
        self.track_templates = [TrackTemplate(self.template, self.runtime_variables)]
        self.result_info = async_track_template_result(self.react.hass, self.track_templates, self.async_update_template)
        self.async_refresh()

    
    def destroy(self) -> None:
        super().destroy()
        if self.result_info:
            self.result_info.async_remove()


    @callback
    def async_refresh(self):
        if self.result_info:
            self.tctx.build(self.runtime_variables)
            self.result_info.async_refresh()


    @callback
    def async_update_template(self, event: Union[Event, None], updates: list[TrackTemplateResult]):
        if updates and len(updates) > 0:
            result = updates.pop().result
            if isinstance(result, TemplateError):
                self.react.log.error(f"Config: Error rendering {self.property}: {result}")
                return

            self.owner.set_property(self.property, self.type_converter(result))
            self.async_update()
