---
title: FieldSurvey_20240610-14_PA
---

# FieldSurvey_20240610-14_PA

- **Survey Date**: 10/06/2024 - 14/06/2024
- **Member**: IBAMA: 4 / JICA: 3 / JAXA: 2 / JICA HQs:2
- **Map**: 
![[FieldSurvey_20240610-14_PA.png]]

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
  const TARGET_SURVEY_ID = "FieldSurvey_20240610-14_PA";

  // トップと同じ GeoJSON を使う
  const GEOJSON_URL = "../../assets/MORI_survey_github.geojson";

  // ===== 地図初期化 =====
  const map = L.map("map").setView([-9.0, -63.0], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  function filterBySurveyId(geojson, surveyId) {
    const feats = (geojson && geojson.features) ? geojson.features : [];
    const filtered = feats.filter((f) => {
      const p = (f && f.properties) || {};
      return (p.title || "") === surveyId;
    });
    return { ...geojson, features: filtered };
  }

  fetch(GEOJSON_URL)
    .then((r) => {
      if (!r.ok) throw new Error("GeoJSON load failed: " + r.status);
      return r.json();
    })
    .then((data) => {
      const filtered = filterBySurveyId(data, TARGET_TITLE);

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
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          let html = "";

          if (p.title) html += "<b>" + p.title + "</b><br>";

          if (p.survey_id) {
            const id = String(p.survey_id).trim();
            const href = "./" + encodeURIComponent(id) + "/"; // ★ md直置き想定のURL
            html += 'Survey ID: <a href="' + href + '">' + id + "</a><br>";
          }

          if (p.region) html += "Mesh: " + p.region + "<br>";
          if (p.survey_date) html += "Date: " + p.survey_date + "<br>";

          if (html) layer.bindPopup(html);
        },
      }).addTo(map);

      if (layer.getBounds().isValid()) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] });
      } else {
        console.warn("No points found for survey_id:", TARGET_TITLE);
      }
    })
    .catch((e) => console.error(e));
</script>
---

## Suevey id list
| ID | Mesh |
|--------|------|
| [AL-PA-2406-01](./AL-PA-2406-01) | S02W052 |
| [AL-PA-2406-03](./AL-PA-2406-03) | S02W052 |
| [AL-PA-2406-04Ref](./AL-PA-2406-04Ref) | S02W052 |
| [AL-PA-2406-05](./AL-PA-2406-05) | S02W052 |
| [AL-PA-2406-06](./AL-PA-2406-06) | S02W052 |
| [ST-PA-2406-01a](./ST-PA-2406-01a) | S03W054 |
| [ST-PA-2406-01b](./ST-PA-2406-01b) | S03W054 |
| [ST-PA-2406-02](./ST-PA-2406-02) | S02W055 |
| [ST-PA-2406-03Ref](./ST-PA-2406-03Ref) | S03W054 |
| [ST-PA-2406-04Ref](./ST-PA-2406-04Ref) | S03W054 |
| [ST-PA-2406-08](./ST-PA-2406-08) | S02W055 |
| [ST-PA-2406-09](./ST-PA-2406-09) | S02W055 |
| [ST-PA-2406-10](./ST-PA-2406-10) | S02W055 |
| [ST-PA-2406-11Ref](./ST-PA-2406-11Ref) | S02W055 |
