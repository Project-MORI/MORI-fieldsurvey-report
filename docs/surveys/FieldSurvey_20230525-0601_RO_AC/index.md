---
title: FieldSurvey_20230525-0601_RO_AC
---

# FieldSurvey_20230525-0601_RO_AC

- **Survey Date**: 25/05/2023 - 01/06/2023
- **Member**: IBAMA: 4 / JICA: 2 / JAXA: 2
- **Map**: 
![[FieldSurvey_20230525-0601_RO_AC.png]]
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
  const TARGET_TITLE = "FieldSurvey_20230525-0601_RO_AC";

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
| [AB-RO-2305-01a](./AB-RO-2305-01a) | S09W067 |
| [AB-RO-2305-01b](./AB-RO-2305-01b) | S09W067 |
| [AB-RO-2305-02](./AB-RO-2305-02) | S09W066 |
| [AB-RO-2305-03](./AB-RO-2305-03) | S09W067 |
| [AB-RO-2305-04a](./AB-RO-2305-04a) | S09W067 |
| [AB-RO-2305-04b](./AB-RO-2305-04b) | S09W067 |
| [AB-RO-2305-04c](./AB-RO-2305-04c) | S09W067 |
| [AB-RO-2305-05](./AB-RO-2305-05) | S09W066 |
| [AB-RO-2305-06a](./AB-RO-2305-06a) | S09W066 |
| [AB-RO-2305-06b](./AB-RO-2305-06b) | S09W066 |
| [BA-AM-2305-36](./BA-AM-2305-36) | S09W068 |
| [BA-AM-2305-37](./BA-AM-2305-37) | S09W068 |
| [EX-RO-2305-07](./EX-RO-2305-07) | S09W067 |
| [EX-RO-2305-08](./EX-RO-2305-08) | S09W067 |
| [EX-RO-2305-10](./EX-RO-2305-10) | S09W067 |
| [EX-RO-2305-21](./EX-RO-2305-21) | S09W067 |
| [EX-RO-2305-22](./EX-RO-2305-22) | S09W067 |
| [EX-RO-2305-23](./EX-RO-2305-23) | S09W067 |
| [EX-RO-2305-23b](./EX-RO-2305-23b) | S09W067 |
| [EX-RO-2305-39](./EX-RO-2305-39) | S09W067 |
| [RB-AC-2305-28](./RB-AC-2305-28) | S09W068 |
| [RB-AC-2305-38](./RB-AC-2305-38) | S09W068 |
