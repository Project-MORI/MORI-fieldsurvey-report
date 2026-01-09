---
title: FieldSurvey_20240205-06_PA
---

# FieldSurvey_20240205-06_PA

- **Survey Date**: 
- **Member**: 
- **Map**: 
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
  const TARGET_SURVEY_ID = "FieldSurvey_20240205-06_PA";

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
| [AL-PA-2402-01](./AL-PA-2402-01) | S02W052 |
| [AL-PA-2402-02](./AL-PA-2402-02) | S02W052 |
| [AL-PA-2402-03](./AL-PA-2402-03) | S02W052 |
| [AL-PA-2402-04Ref](./AL-PA-2402-04Ref) | S02W052 |
| [AL-PA-2402-05Ref](./AL-PA-2402-05Ref) | S02W052 |
| [AL-PA-2402-06Ref](./AL-PA-2402-06Ref) | S02W052 |
| [AL-PA-2402-07Ref](./AL-PA-2402-07Ref) | S02W052 |
| [AL-PA-2402-08Ref](./AL-PA-2402-08Ref) | S02W052 |
| [AL-PA-2402-09](./AL-PA-2402-09) | S02W052 |
| [AL-PA-2402-10Ref](./AL-PA-2402-10Ref) | S02W052 |
| [AL-PA-2402-11a](./AL-PA-2402-11a) | S02W052 |
| [AL-PA-2402-11b](./AL-PA-2402-11b) | S02W052 |
| [AL-PA-2402-12](./AL-PA-2402-12) | S02W052 |
| [AL-PA-2402-13Ref](./AL-PA-2402-13Ref) | S02W052 |
| [AL-PA-2402-14](./AL-PA-2402-14) | S02W052 |
| [AL-PA-2402-15Ref](./AL-PA-2402-15Ref) | S02W052 |
| [AL-PA-2402-16](./AL-PA-2402-16) | S02W052 |
| [AL-PA-2402-17](./AL-PA-2402-17) | S02W052 |
| [AL-PA-2402-19](./AL-PA-2402-19) | S02W052 |
| [AL-PA-2402-20](./AL-PA-2402-20) | S02W052 |
| [AL-PA-2402-21Ref](./AL-PA-2402-21Ref) | S02W052 |
| [AL-PA-2402-22](./AL-PA-2402-22) | S02W052 |
| [AL-PA-2402-23Ref](./AL-PA-2402-23Ref) | S02W052 |
| [AL-PA-2402-24](./AL-PA-2402-24) | S02W052 |
| [AL-PA-2402-25](./AL-PA-2402-25) | S02W052 |
| [AL-PA-2402-26](./AL-PA-2402-26) | S02W052 |
| [AL-PA-2402-27Ref](./AL-PA-2402-27Ref) | S02W052 |
| [ST-PA-2402-01](./ST-PA-2402-01) | S02W055 |
| [ST-PA-2402-02](./ST-PA-2402-02) | S02W055 |
| [ST-PA-2402-03](./ST-PA-2402-03) | S02W055 |
| [ST-PA-2402-04](./ST-PA-2402-04) | S02W052 |
| [ST-PA-2402-05](./ST-PA-2402-05) | S02W052 |
| [ST-PA-2402-06](./ST-PA-2402-06) | S02W052 |
| [ST-PA-2402-07](./ST-PA-2402-07) | S02W052 |
| [ST-PA-2402-08](./ST-PA-2402-08) | S02W052 |
| [ST-PA-2402-09](./ST-PA-2402-09) | S03W054 |
| [ST-PA-2402-10](./ST-PA-2402-10) | S03W054 |
| [ST-PA-2402-11](./ST-PA-2402-11) | S03W054 |
| [ST-PA-2402-12](./ST-PA-2402-12) | S03W054 |
| [ST-PA-2402-13](./ST-PA-2402-13) | S03W054 |
| [ST-PA-2402-14](./ST-PA-2402-14) | S03W054 |
| [ST-PA-2402-15](./ST-PA-2402-15) | S03W054 |
| [ST-PA-2402-16](./ST-PA-2402-16) | S03W054 |
| [ST-PA-2402-17](./ST-PA-2402-17) | S03W054 |
| [ST-PA-2402-18](./ST-PA-2402-18) | S03W054 |
| [ST-PA-2402-19](./ST-PA-2402-19) | S03W054 |
| [ST-PA-2402-20](./ST-PA-2402-20) | S03W054 |
