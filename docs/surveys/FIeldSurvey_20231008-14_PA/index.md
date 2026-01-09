---
title: FIeldSurvey_20231008-14_PA
---

# FIeldSurvey_20231008-14_PA

- **Survey Date**: 08/10/2023 - 14/10/2023
- **Member**: IBAMA: 3 / JICA: 2
- **Map**: 
![[FIeldSurvey_20231008-14_PA.png]]

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
  const TARGET_TITLE = "FieldSurvey_20231008-14_PA";

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
| [AL-PA-2310-03](./AL-PA-2310-03) | S02W052 |
| [AL-PA-2310-05](./AL-PA-2310-05) | S02W052 |
| [AL-PA-2310-06](./AL-PA-2310-06) | S02W052 |
| [AL-PA-2310-07](./AL-PA-2310-07) | S02W052 |
| [AL-PA-2310-10](./AL-PA-2310-10) | S02W052 |
| [AL-PA-2310-11](./AL-PA-2310-11) | S02W052 |
| [AL-PA-2310-13](./AL-PA-2310-13) | S02W052 |
| [AL-PA-2310-18](./AL-PA-2310-18) | S02W052 |
| [AL-PA-2310-19](./AL-PA-2310-19) | S02W052 |
| [AL-PA-2310-23](./AL-PA-2310-23) | S02W052 |
| [AL-PA-2310-24](./AL-PA-2310-24) | S02W052 |
| [AL-PA-2310-30](./AL-PA-2310-30) | S02W052 |
| [AL-PA-2310-35](./AL-PA-2310-35) | S02W052 |
| [AL-PA-2310-40](./AL-PA-2310-40) | S02W052 |
| [AL-PA-2310-42](./AL-PA-2310-42) | S02W052 |
| [AL-PA-2310-49](./AL-PA-2310-49) | S02W052 |
| [AL-PA-2310-50](./AL-PA-2310-50) | S02W052 |
