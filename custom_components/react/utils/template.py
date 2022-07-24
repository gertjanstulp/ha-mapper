from typing import Any, Union

from homeassistant.core import Event, callback
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.event import TrackTemplate, TrackTemplateResult, async_track_template_result
from homeassistant.helpers.template import Template

from ..base import ReactBase
from .updatable import Updatable, callable_type
from .context import TemplateContext, TemplateContextDataProvider


class ValueJitter:
    def __init__(self, value: Any, type_converter: Any = None) -> None:
        self.value = value
        self.type_converter = type_converter

    
    def render(self, *args):
        if self.type_converter:
            return self.type_converter(self.value)
        else:
            return self.value


class TemplateJitter:
    owner: Union[Any, None] = None
    react: ReactBase
    property: str
    type_converter: Any
    template: Template


    def __init__(self, react: ReactBase, property: str, template: Template, type_converter: Any, template_context: TemplateContext):
        self.property = property
        self.template = template
        self.type_converter = type_converter
        self.template_context = template_context

        template.hass = react.hass


    def render(self, template_context_data_provider: TemplateContextDataProvider):
        result = None
        try:
            self.template_context.build(template_context_data_provider)
            result = self.template.async_render(self.template_context.runtime_variables)
        except TemplateError as te:
            self.react.log.error(f"Config: Error rendering {self.property}: {result}")
        return result


class TemplateTracker(Updatable):
    
    owner: Union[Any, None] = None
    react: ReactBase
    property: str
    type_converter: Any
    template: Template
    template_context: Union[TemplateContext, None] = None


    def __init__(self, react: ReactBase, owner: Any, property: str, template: Template, type_converter: Any, template_context: TemplateContext, update_callback: callable_type = None):
        super().__init__(react)
        self.react = react
        self.owner = owner
        self.property = property
        self.template = template
        self.type_converter = type_converter
        self.template_context = template_context

        template.hass = react.hass
        if update_callback:
            self.on_update(update_callback)


    def start(self):
        setattr(self.owner, self.property, None)
        self.template_context.build()
        self.track_templates = [TrackTemplate(self.template, self.template_context.runtime_variables)]
        self.result_info = async_track_template_result(self.react.hass, self.track_templates, self.async_update_template)
        self.async_refresh()

    
    def destroy(self):
        if self.result_info:
            self.result_info.async_remove()


    @callback
    def async_refresh(self):
        if self.result_info:
            self.template_context.build()
            self.result_info.async_refresh()


    @callback
    def async_update_template(self, event: Union[Event, None], updates: list[TrackTemplateResult]):
        if updates and len(updates) > 0:
            result = updates.pop().result
            if isinstance(result, TemplateError):
                self.react.log.error(f"Config: Error rendering {self.property}: {result}")
                return

            if hasattr(self.owner, "set_property"):
                self.owner.set_property(self.owner, self.property, self.type_converter(result))
            else:
                setattr(self.owner, self.property, self.type_converter(result))
            self.async_update()
