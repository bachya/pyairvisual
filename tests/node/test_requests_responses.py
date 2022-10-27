"""Define tests for Node errors."""
# pylint: disable=unused-argument
import pytest

from pyairvisual.node import NodeSamba

from tests.common import TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD


@pytest.mark.asyncio
async def test_duplicate_connection(caplog, setup_samba_connection):
    """Test attempting to connect after we're already connected."""
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    await node.async_connect()
    await node.async_connect()
    await node.async_disconnect()

    assert any("Already connected!" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_duplicate_disconnection(caplog, setup_samba_connection):
    """Test attempting to disconnect after we're already disconnected."""
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    await node.async_connect()
    await node.async_disconnect()
    await node.async_disconnect()

    assert any("Already disconnected!" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_node_by_samba_dict_response(setup_samba_connection):
    """Test getting a node's info over the local network (via Samba).

    This variant of the test expects a dictionary-esque response from the unit.
    """
    async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
        measurements = await node.async_get_latest_measurements()
        history = await node.async_get_history()

    assert len(history["measurements"]) == 7
    assert measurements["last_measurement_timestamp"] == 1584204767
    assert measurements["measurements"]["co2"] == "442"
    assert measurements["measurements"]["humidity"] == "35"
    assert measurements["measurements"]["pm0_1"] == "3"
    assert measurements["measurements"]["pm1_0"] == "4"
    assert measurements["measurements"]["aqi_cn"] == "6"
    assert measurements["measurements"]["aqi_us"] == "17"
    assert measurements["measurements"]["pm2_5"] == "4.0"
    assert measurements["measurements"]["temperature_C"] == "19.3"
    assert measurements["measurements"]["temperature_F"] == "66.8"
    assert measurements["measurements"]["voc"] == "-1"

    assert history["trends"] == {
        "aqi_cn": "decreasing",
        "aqi_us": "decreasing",
        "co2": "decreasing",
        "humidity": "increasing",
        "pm0_1": "decreasing",
        "pm1_0": "decreasing",
        "pm2_5": "decreasing",
        "voc": "flat",
    }


@pytest.mark.asyncio
async def test_node_by_samba_fewer_trend_measurements(setup_samba_connection):
    """Test getting a node's trends with a configured number of measurements."""
    async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
        history = await node.async_get_history(measurements_to_use=3)

    assert history["trends"] == {
        "aqi_cn": "flat",
        "aqi_us": "flat",
        "co2": "decreasing",
        "humidity": "decreasing",
        "pm0_1": "flat",
        "pm1_0": "decreasing",
        "pm2_5": "flat",
        "voc": "flat",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "node_measurements_file", ["node_measurements_samba_list_response.json"]
)
async def test_node_by_samba_list_response(setup_samba_connection):
    """Test getting a node's info over the local network (via Samba).

    This variant of the test expects a list-esque response from the unit.
    """
    async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
        measurements = await node.async_get_latest_measurements()
        history = await node.async_get_history()

    assert len(history["measurements"]) == 7
    assert measurements["last_measurement_timestamp"] == 1584204767
    assert measurements["measurements"]["co2"] == "442"
    assert measurements["measurements"]["humidity"] == "35"
    assert measurements["measurements"]["pm0_1"] == "3"
    assert measurements["measurements"]["pm1_0"] == "4"
    assert measurements["measurements"]["aqi_cn"] == "6"
    assert measurements["measurements"]["aqi_us"] == "17"
    assert measurements["measurements"]["pm2_5"] == "4.0"
    assert measurements["measurements"]["temperature_C"] == "19.3"
    assert measurements["measurements"]["temperature_F"] == "66.8"
    assert measurements["measurements"]["voc"] == "-1"

    assert history["trends"] == {
        "aqi_cn": "decreasing",
        "aqi_us": "decreasing",
        "co2": "decreasing",
        "humidity": "increasing",
        "pm0_1": "decreasing",
        "pm1_0": "decreasing",
        "pm2_5": "decreasing",
        "voc": "flat",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "node_measurements_file", ["node_measurements_samba_no_sensor_life_response.json"]
)
async def test_node_by_samba_no_sensor_life_data(setup_samba_connection):
    """Test a proper response when no sensor life values are returned."""
    async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
        measurements = await node.async_get_latest_measurements()

    assert measurements["status"]["sensor_life"] == {}
