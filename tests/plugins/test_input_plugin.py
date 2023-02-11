import pytest

from homeassistant.core import HomeAssistant
from homeassistant.components.input_number import (
    ATTR_VALUE
)
from homeassistant.const import (
    ATTR_ENTITY_ID, 
    STATE_ON,
    STATE_OFF,
    STATE_UNKNOWN,
)

from custom_components.react.base import ReactBase
from custom_components.react.const import ATTR_ENTITY, ATTR_PLUGIN_MODULE, ATTR_STATE, DOMAIN

from tests.common import FIXTURE_WORKFLOW_NAME, TEST_CONTEXT
from tests.tst_context import TstContext


@pytest.mark.asyncio
@pytest.mark.parametrize(FIXTURE_WORKFLOW_NAME, ["input_number_set"])
async def test_input_number_set(hass: HomeAssistant, workflow_name, react_component):
    """
    Test for input plugin
    """

    mock_plugin = {ATTR_PLUGIN_MODULE: "tests._plugins.input_plugin_input_number_set_mock"}
    comp = await react_component
    await comp.async_setup(workflow_name, plugins=[mock_plugin])
    react: ReactBase = hass.data[DOMAIN]
    
    plugin_data = {
        ATTR_ENTITY_ID: "input_number_set_test",
        ATTR_VALUE: 12.34
    }

    tc = TstContext(hass, workflow_name)
    react.hass.data[TEST_CONTEXT] = tc
    async with tc.async_listen_reaction_event():
        tc.verify_reaction_not_found()
        await tc.async_send_action_event()
        tc.verify_reaction_not_found()
        await tc.async_verify_reaction_event_received()
        tc.verify_trace_record()
        
        tc.verify_plugin_data_sent()
        tc.verify_plugin_data_content(plugin_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(FIXTURE_WORKFLOW_NAME, ["input_boolean_turn_on"])
async def test_input_boolean_turn_on(hass: HomeAssistant, workflow_name, react_component):
    """
    Test for input plugin
    """

    mock_plugin = {ATTR_PLUGIN_MODULE: "tests._plugins.input_plugin_input_boolean_turn_on_mock"}
    comp = await react_component
    await comp.async_setup(workflow_name, plugins=[mock_plugin])
    react: ReactBase = hass.data[DOMAIN]
    
    plugin_data = {
        ATTR_ENTITY_ID: "input_boolean_turn_on_test",
        ATTR_STATE: STATE_ON
    }

    tc = TstContext(hass, workflow_name)
    react.hass.data[TEST_CONTEXT] = tc
    async with tc.async_listen_reaction_event():
        tc.verify_reaction_not_found()
        await tc.async_send_action_event()
        tc.verify_reaction_not_found()
        await tc.async_verify_reaction_event_received()
        tc.verify_trace_record()
        
        tc.verify_plugin_data_sent()
        tc.verify_plugin_data_content(plugin_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(FIXTURE_WORKFLOW_NAME, ["input_boolean_turn_off"])
async def test_input_boolean_turn_off(hass: HomeAssistant, workflow_name, react_component):
    """
    Test for input plugin
    """

    mock_plugin = {ATTR_PLUGIN_MODULE: "tests._plugins.input_plugin_input_boolean_turn_off_mock"}
    comp = await react_component
    await comp.async_setup(workflow_name, plugins=[mock_plugin])
    react: ReactBase = hass.data[DOMAIN]
    
    plugin_data = {
        ATTR_ENTITY_ID: "input_boolean_turn_off_test",
        ATTR_STATE: STATE_OFF
    }

    tc = TstContext(hass, workflow_name)
    react.hass.data[TEST_CONTEXT] = tc
    async with tc.async_listen_reaction_event():
        tc.verify_reaction_not_found()
        await tc.async_send_action_event()
        tc.verify_reaction_not_found()
        await tc.async_verify_reaction_event_received()
        tc.verify_trace_record()
        
        tc.verify_plugin_data_sent()
        tc.verify_plugin_data_content(plugin_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(FIXTURE_WORKFLOW_NAME, ["input_boolean_toggle"])
async def test_input_boolean_toggle(hass: HomeAssistant, workflow_name, react_component):
    """
    Test for input plugin
    """

    mock_plugin = {ATTR_PLUGIN_MODULE: "tests._plugins.input_plugin_input_boolean_toggle_mock"}
    comp = await react_component
    await comp.async_setup(workflow_name, plugins=[mock_plugin])
    react: ReactBase = hass.data[DOMAIN]
    
    plugin_data = {
        ATTR_ENTITY_ID: "input_boolean_toggle_test",
        ATTR_STATE: STATE_UNKNOWN
    }

    tc = TstContext(hass, workflow_name)
    react.hass.data[TEST_CONTEXT] = tc
    async with tc.async_listen_reaction_event():
        tc.verify_reaction_not_found()
        await tc.async_send_action_event()
        tc.verify_reaction_not_found()
        await tc.async_verify_reaction_event_received()
        tc.verify_trace_record()
        
        tc.verify_plugin_data_sent()
        tc.verify_plugin_data_content(plugin_data)

