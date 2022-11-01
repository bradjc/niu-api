# NIU API

A wrapper script for the NIU API.

This is an open source project and still under construction.
It may take some time to complete this project ;-).

## Example

### CLI

```
niu-api trips.detailed_date date=20221028
```

### API

```python
scooters = niuApi.apicommands.v5.scooter_list()

for scooter in scooters:
    sn = scooter["sn_id"]

    metadata = {
        "device_id": sn,
        "sku": scooter["sku_name"],
        "name": scooter["scooter_name"],
        "type_": scooter["product_type"],
        "carframe_id": scooter["carframe_id"],
    }

    detail = niuApi.apicommands.v5.scooter_detail(sn)

    metadata["engine_num"] = detail["engine_num"]
    data = {
        "battery_%": detail["battery_level"],
        "battery_cycles": detail["battery_cycle"],
        "range_mi": km_to_mi(detail["estimated_mileage"]),
    }

    mileage = niuApi.apicommands.other.motoinfo_overallTally(sn)
    data["odometer_mi"] = km_to_mi(mileage["totalMileage"])

    print(metadata)
    print(data)

    trips = niuApi.apicommands.v5.track_list_v2(sn)
    for trip in trips["items"]:
        print(trip)
```


## Finding APIs

I followed the guide here:
https://sayfer.io/blog/how-to-set-up-a-proxy-in-android-using-mitm-proxydroid/
to view the API calls.
