import json
import logging
import voluptuous as vol
from datetime import datetime
from datetime import timedelta
from mnb import Mnb

from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity, generate_entity_id
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = [ ]

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "Data provided by mnb.hu"
CONF_CURRENCIES = 'currencies'

DEFAULT_ICON = 'mdi:cash'

SCAN_INTERVAL = timedelta(hours=3)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CURRENCIES, default=[]): vol.All(cv.ensure_list, [cv.string]),
})

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    currencies = config.get(CONF_CURRENCIES)

    _mnb_currencies = await async_get_currencies(hass)
    _LOGGER.debug("mnb currencies: " + str(_mnb_currencies))

    _cdata = await async_get_cdata(hass)
    _LOGGER.debug("mnb rates:" + str(_cdata))

    for currency in currencies:
      if currency.upper() in _mnb_currencies:
        _LOGGER.debug("checking currency: " + str(currency))
        if 'rates' in _cdata:
          for item in _cdata['rates']:
            if item.get('currency') != currency.upper():
              continue
            _LOGGER.debug("found: " + item.get('currency') + ": " + str(item.get('rate')))
            async_add_devices(
              [MNBCurrencySensor(hass, currency, item.get('rate'))],update_before_add=True)
            break

async def async_get_cdata(hass):
    cjson = {}

    client = await hass.async_add_executor_job(Mnb)
    p3 = await hass.async_add_executor_job(client.get_current_exchange_rates)
    cjson = json.loads(p3.to_json())

    return cjson

async def async_get_currencies(hass):
    client = await hass.async_add_executor_job(Mnb)
    p3 = await hass.async_add_executor_job(client.get_currencies)

    return p3

class MNBCurrencySensor(Entity):

    def __init__(self, hass, currency, rate ):
        """Initialize the sensor."""
        self._hass = hass
        self._state = rate
        self._last_poll = ""
        self._cdata = []
        self._currency = currency.upper()
        self._name = "mnb_" + currency.lower()
        self.entity_id = generate_entity_id(ENTITY_ID_FORMAT, self._name, None, hass)

        self._icon = DEFAULT_ICON

    @property
    def extra_state_attributes(self):
        attr = {}

        attr["provider"] = CONF_ATTRIBUTION
        attr["last_poll"] = self._last_poll
        return attr

    async def async_update(self):

        self._cdata = await async_get_cdata(self._hass)
        if len(self._cdata) == 0:
            self._state = 1
        else:
          for item in self._cdata['rates']:
            if item.get('currency') != self._currency:
              continue
            self._state = item.get('rate')
            break

        dt_now = datetime.now()
        self._last_poll = dt_now.strftime("%Y/%m/%d %H:%M")

        return self._state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return DEFAULT_ICON
