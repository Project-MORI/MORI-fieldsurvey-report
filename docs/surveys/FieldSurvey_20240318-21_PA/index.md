---
title: FieldSurvey_20240318-21_PA
---

# FieldSurvey_20240318-21_PA

- **Survey Date**: 18/03/2024 - 21/03/2024
- **Member**: IBAMA: 5 / JICA: 3 / JICA BR: 1
- **Map**: 
![[FieldSurvey_20240318-21_PA.png]]
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
  const TARGET_TITLE = "FieldSurvey_20240318_PA";

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
| [AL-PA-2403-01](./AL-PA-2403-01) | S02W052 |
| [AL-PA-2403-02](./AL-PA-2403-02) | S02W052 |
| [AL-PA-2403-09](./AL-PA-2403-09) | S02W052 |
| [AL-PA-2403-16Ref](./AL-PA-2403-16Ref) | S03W053 |
| [AL-PA-2403-17Ref](./AL-PA-2403-17Ref) | S02W053 |
| [AL-PA-2403-18](./AL-PA-2403-18) | S02W053 |
| [AL-PA-2403-19](./AL-PA-2403-19) | S02W052 |
