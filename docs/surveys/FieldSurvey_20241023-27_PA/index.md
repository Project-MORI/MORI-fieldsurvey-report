---
title: FieldSurvey_20241023-27_PA
---

# FieldSurvey_20241023-27_PA

- **Survey Date**: 23/10/2024 - 27/10/2024
- **Member**: JICA: 2
- **Map**: 
![[FieldSurvey_20241023-27_PA.png]]
---
## point Map
<div id="map"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>
  #map {
    height: 450px;
    margin: 1rem 0;
  }
</style>

<script>
  // ===== このページ専用設定 =====
  const TARGET_SURVEY_ID = "FieldSurvey_20241023-27_PA";

  // トップと同じ GeoJSON を使う
  const GEOJSON_URL = "../../assets/MORI_survey_github.geojson";

  // ===== 地図初期化 =====
  const map = L.map("map").setView([-9.0, -63.0], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // ===== survey_id で GeoJSON をフィルタ =====
  function filterBySurveyId(geojson, surveyId) {
    if (!geojson || !geojson.features) return geojson;

    const filtered = geojson.features.filter((f) => {
      const p = f.properties || {};
      return p.survey_id === surveyId;
    });

    return { ...geojson, features: filtered };
  }

  // ===== GeoJSON 読み込み =====
  fetch(GEOJSON_URL)
    .then((r) => {
      if (!r.ok) throw new Error("GeoJSON load failed");
      return r.json();
    })
    .then((data) => {
      const filtered = filterBySurveyId(data, TARGET_SURVEY_ID);

      const layer = L.geoJSON(filtered, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 7,
            fillColor: "#e41a1c",
            color: "#000",
            weight: 1,
            fillOpacity: 0.9,
          });
        },

        onEachFeature: function (feature, layer) {
          const p = feature.properties || {};
          let html = "";
          if (p.survey_id) html += "<b>" + p.survey_id + "</b><br>";
          if (p.region) html += "Mesh: " + p.region + "<br>";
          if (p.survey_date) html += "Date: " + p.survey_date + "<br>";
          layer.bindPopup(html);
        },
      }).addTo(map);

      if (layer.getBounds().isValid()) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] });
      }
    })
    .catch((e) => {
      console.error(e);
    });
</script>
---

## Suevey id list
| ID | Mesh |
|--------|------|
| [NP-PA-2410-01](./NP-PA-2410-01) | S07W056 |
| [NP-PA-2410-03](./NP-PA-2410-03) | S07W056 |
| [NP-PA-2410-04](./NP-PA-2410-04) | S07W056 |
| [NP-PA-2410-05](./NP-PA-2410-05) | S07W056 |
| [NP-PA-2410-06](./NP-PA-2410-06) | S07W056 |
| [NP-PA-2410-07](./NP-PA-2410-07) | S07W056 |
| [NP-PA-2410-08](./NP-PA-2410-08) | S07W056 |
| [NP-PA-2410-12](./NP-PA-2410-12) | S07W056 |
| [NP-PA-2410-14](./NP-PA-2410-14) | S07W056 |
| [NP-PA-2410-15](./NP-PA-2410-15) | S07W056 |
| [NP-PA-2410-16](./NP-PA-2410-16) | S07W056 |
| [NP-PA-2410-17](./NP-PA-2410-17) | S07W056 |
| [NP-PA-2410-21](./NP-PA-2410-21) | S07W056 |
| [NP-PA-2410-22](./NP-PA-2410-22) | S07W056 |
| [NP-PA-2410-23](./NP-PA-2410-23) | S07W056 |
| [NP-PA-2410-24](./NP-PA-2410-24) | S07W056 |
| [NP-PA-2410-25](./NP-PA-2410-25) | S07W056 |
| [NP-PA-2410-26](./NP-PA-2410-26) | S07W056 |
| [NP-PA-2410-29](./NP-PA-2410-29) | S07W056 |
| [NP-PA-2410-30](./NP-PA-2410-30) | S07W056 |
| [NP-PA-2410-31](./NP-PA-2410-31) | S07W056 |
| [NP-PA-2410-32](./NP-PA-2410-32) | S06W055 |
| [NP-PA-2410-36](./NP-PA-2410-36) | S07W056 |
| [NP-PA-2410-37](./NP-PA-2410-37) | S07W056 |
| [NP-PA-2410-38](./NP-PA-2410-38) | S07W056 |
| [NP-PA-2410-40](./NP-PA-2410-40) | S06W056 |
| [NP-PA-2410-41](./NP-PA-2410-41) | S06W056 |
| [NP-PA-2410-42](./NP-PA-2410-42) | S07W056 |
| [NP-PA-2410-43](./NP-PA-2410-43) | S07W056 |
| [NP-PA-2410-44](./NP-PA-2410-44) | S07W056 |
| [NP-PA-2410-45](./NP-PA-2410-45) | S07W056 |
| [NP-PA-2410-46](./NP-PA-2410-46) | S07W056 |
| [NP-PA-2410-47](./NP-PA-2410-47) | S07W056 |
| [NP-PA-2410-49](./NP-PA-2410-49) | S06W056 |
| [NP-PA-2410-51](./NP-PA-2410-51) | S06W056 |
| [NP-PA-2410-52Ref](./NP-PA-2410-52Ref) | S06W055 |
| [NP-PA-2410-53](./NP-PA-2410-53) | S07W056 |
