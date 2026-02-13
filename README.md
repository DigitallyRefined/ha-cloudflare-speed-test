# Cloudflare Speed Test for Home Assistant

[![Validate with hassfest](https://github.com/DigitallyRefined/ha-cloudflare-speed-test/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/DigitallyRefined/ha-cloudflare-speed-test/actions/workflows/hassfest.yaml)
[![HACS Validate](https://github.com/DigitallyRefined/ha-cloudflare-speed-test/actions/workflows/hacs_action.yml/badge.svg)](https://github.com/DigitallyRefined/ha-cloudflare-speed-test/actions/workflows/hacs_action.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/custom-components/hacs)

![downloads](https://img.shields.io/github/downloads/DigitallyRefined/ha-cloudflare-speed-test/total.svg)
![downloads](https://img.shields.io/github/downloads/DigitallyRefined/ha-cloudflare-speed-test/latest/total.svg)

This integration uses the [cloudflarepycli](https://pypi.org/project/cloudflarepycli/) Python library to retrieve network performance statistics from [https://speed.cloudflare.com](https://speed.cloudflare.com) including:

* 90th percentile down/up
* 25MB down
* 10MB down/up
* 1MB down/up
* 100kB down/up
* Latency
* Jitter
* ISP
* IP address

It also attaches the test servers city, region and code to each result.

## Installation

### Using HACS  

If you dont' have [HACS](https://hacs.xyz) installed yet, I highly recommend it.  

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DigitallyRefined&repository=ha-cloudflare-speed-test&category=integration)  
Or search for `Cloudflare Speed Test` in HACS or copy this GitHub URL and add it as a custom integration repository.

### Manual  

[Download the latest `cloudflare_speed_test.zip` release](https://github.com/DigitallyRefined/ha-cloudflare-speed-test/releases) and extract it into your `<config>/custom_component` folder.

### Setup

After installation you need to **restart** Home Assistant before using this integration.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=cloudflare_speed_test)  
Or go to **Settings** -> **Devices & Services**  
Click **Add integration** and search for `Cloudflare Speed Test`

## Configuration

By default, a speed test will be run every hour or you can set a custom interval.

If you want to select an exact time when the speed test should run (e.g. to be more specific such as once a day over night) you can disable the default polling interval and create your own timed automation.

To disable polling and create your own timed automation:

1. Go to **Settings** > **Devices & services**, and select the Cloudflare Speed Test integration.
2. On the integration entry, select the hamburger menu icon
   * Then, select **System options** and toggle the button to disable polling.
3. To define your custom polling interval, create an automation.
   1. Go to [**Settings** > **Automations & scenes**](https://my.home-assistant.io/redirect/automations) and create a new automation.
   2. Define any triggers/conditions you like (e.g. a time trigger).
   3. Select **Add action**, then, search/select **Perform action**.
   4. Search/select the [`homeassistant.update_entity` action](https://www.home-assistant.io/integrations/homeassistant/#action-homeassistantupdate_entity).
   5. Search/select the `cloudflare_speed_test_90th_percentile_down` entity (note: you only need to select one Cloudflare entity, the other entities will be automatically updated).
4. Save the automation to automatically trigger based on your own schedule.

### Add to dashboard

![Graph screenshot](screenshot.webp)

To add graphs to your dashboard, the following YAML can be used in a manual card:

<details>
<summary>Expand for dashboard YAML</summary>

```yaml
type: vertical-stack
cards:
  - chart_type: line
    period: day
    type: statistics-graph
    entities:
      - sensor.cloudflare_speed_test_90th_percentile_down
      - sensor.cloudflare_speed_test_25mb_down
      - sensor.cloudflare_speed_test_10mb_down
      - sensor.cloudflare_speed_test_1mb_down
      - sensor.cloudflare_speed_test_100kb_down
    stat_types:
      - max
    title: Download speed
  - chart_type: line
    period: day
    type: statistics-graph
    entities:
      - sensor.cloudflare_speed_test_90th_percentile_up
      - sensor.cloudflare_speed_test_10mb_up
      - sensor.cloudflare_speed_test_1mb_up
      - sensor.cloudflare_speed_test_100kb_up
    stat_types:
      - max
    title: Upload speed
  - chart_type: line
    period: day
    type: statistics-graph
    entities:
      - sensor.cloudflare_speed_test_latency
      - sensor.cloudflare_speed_test_jitter
    stat_types:
      - min
    title: Ping
```
</details>

## Notes

* When running on Raspberry Pi the maximum speed is limited by the LAN adapter. The Raspberry Pi 3+ models come with a Gigabit LAN adapter which supports a [maximum throughput](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) of 300 Mbit/s.
* Running this integration can have negative effects on the system’s performance as it requires a fair amount of memory.
* If run frequently, this integration has the ability to use a considerable amount of data. Frequent updates should be avoided on bandwidth-capped connections.
* While a speed test is running your network capacity is fully utilized. This may have a negative effect on other devices using the network such as gaming consoles or streaming boxes.
* This integration and its author are **not** affiliated or associated with Cloudflare.

## Attribution

Original idea from [@rohankapoorcom, @engrbm87](https://github.com/home-assistant/core/tree/dev/homeassistant/components/speedtestdotnet)
