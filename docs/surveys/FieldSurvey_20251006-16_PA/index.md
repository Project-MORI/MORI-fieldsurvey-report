---
title: FieldSurvey_20251006-16_PA
---

# FieldSurvey_20251006-16_PA

- **Survey Date**: 06/10/2025 - 16/10/2025
- **Member**: IBAMA:6 / JICA: 2 / Media: 4
- **Map**: 
![[FieldSurvey_20251006-16_PA.png]]
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
  const TARGET_SURVEY_ID = "FieldSurvey_20251006-16_PA";

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
| [AL-PA-2510-01](./AL-PA-2510-01) | S02W052 |
| [AL-PA-2510-02](./AL-PA-2510-02) | S03W052 |
| [AL-PA-2510-03](./AL-PA-2510-03) | S02W052 |
| [AL-PA-2510-06](./AL-PA-2510-06) | S02W052 |
| [ST-PA-2510-01](./ST-PA-2510-01) | S03W054 |
| [ST-PA-2510-02](./ST-PA-2510-02) | S03W054 |
| [ST-PA-2510-04](./ST-PA-2510-04) | S02W055 |
| [ST-PA-2510-06](./ST-PA-2510-06) | S03W054 |
| [ST-PA-2510-07](./ST-PA-2510-07) | S03W054 |
| [ST-PA-2510-08](./ST-PA-2510-08) | S03W055 |
| [ST-PA-2510-10](./ST-PA-2510-10) | S03W054 |
| [ST-PA-2510-91](./ST-PA-2510-91) | S03W054 |
| [ST-PA-2510-92](./ST-PA-2510-92) | S03W054 |
| [ST-PA-2510-93](./ST-PA-2510-93) | S03W054 |
| [ST-PA-2510-94](./ST-PA-2510-94) | S03W054 |
| [ST-PA-2510-95](./ST-PA-2510-95) | S03W054 |
