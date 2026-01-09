---
title: FieldSurvey_20220214-21_PA
---

# FieldSurvey_20220214-21_PA

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
  const TARGET_SURVEY_ID = "FieldSurvey_20220214-21_PA";

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
| [AL-PA-2202-01](./AL-PA-2202-01) | S03W052 |
| [AL-PA-2202-02](./AL-PA-2202-02) | S03W052 |
| [AL-PA-2202-03](./AL-PA-2202-03) | S03W052 |
| [AL-PA-2202-07](./AL-PA-2202-07) | S02W052 |
| [AL-PA-2202-08](./AL-PA-2202-08) | S02W053 |
| [AL-PA-2202-09](./AL-PA-2202-09) | S03W053 |
| [AL-PA-2202-10](./AL-PA-2202-10) | S02W053 |
| [AL-PA-2202-11](./AL-PA-2202-11) | S03W052 |
| [AL-PA-2202-12](./AL-PA-2202-12) | S03W052 |
| [AL-PA-2202-13](./AL-PA-2202-13) | S02W052 |
| [AL-PA-2202-14](./AL-PA-2202-14) | S02W052 |
| [AL-PA-2202-15](./AL-PA-2202-15) | S02W052 |
| [AL-PA-2202-16](./AL-PA-2202-16) | S02W052 |
| [AL-PA-2202-17](./AL-PA-2202-17) | S02W052 |
| [AL-PA-2202-18](./AL-PA-2202-18) | S02W052 |
