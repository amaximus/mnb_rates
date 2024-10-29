[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

<p><a href="https://www.buymeacoffee.com/6rF5cQl" rel="nofollow" target="_blank"><img src="https://camo.githubusercontent.com/c070316e7fb193354999ef4c93df4bd8e21522fa/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76312e7376673f6c6162656c3d4275792532306d6525323061253230636f66666565266d6573736167653d25463025394625413525413826636f6c6f723d626c61636b266c6f676f3d6275792532306d6525323061253230636f66666565266c6f676f436f6c6f723d7768697465266c6162656c436f6c6f723d366634653337" alt="Buy me a coffee" data-canonical-src="https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&amp;message=%F0%9F%A5%A8&amp;color=black&amp;logo=buy%20me%20a%20coffee&amp;logoColor=white&amp;labelColor=b0c4de" style="max-width:100%;"></a></p>

# Home Assistant custom component for MNB (Hungarian National Bank) rates

This custom component fetches MNB (Hungarian National Bank) daily exchange rates from mnb.hu.

This custom component requires [https://github.com/belidzs/mnb](https://github.com/belidzs/mnb) package available on PyPI but also set as a python requirement.

#### Installation
The easiest way to install it is through [HACS (Home Assistant Community Store)](https://github.com/hacs/integration),
search for <i>MNB rates</i> in the Integrations.<br />

This platform should be configured as per below information. It will create a sensor for each listed currency named
sensor.mnb_<currency_trigram> (e.g. sensor.mnb_eur, sensor.mnb_usd, etc.)

#### Configuration:
Define sensor with the following configuration parameters:<br />

---
| Name | Optional | `Default` | Description |
| :---- | :---- | :------- | :----------- |
| currencies | **N** | `` | list of currency trigrams to filter on. |
---

#### Example
```
platform: mnb_rates
currencies:
  - EUR
  - USD
```
![MNB rates filtered](https://raw.githubusercontent.com/amaximus/mnb_rates/main/mnb_rates2.png)

## Thanks

Thanks to all the people who have contributed!

[![contributors](https://contributors-img.web.app/image?repo=amaximus/mnb_rates)](https://github.com/amaximus/mnb_rates/graphs/contributors)
