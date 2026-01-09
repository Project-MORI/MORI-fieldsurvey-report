---
title: MORI2_TestSurvey_20250531-0608_RO_AM
---

# MORI2_TestSurvey_20250531-0608_RO_AM

- **Survey Date**: 
- **Member**: 
- **Map**: 
<div id="map"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>
  #map { height: 450px; margin: 1rem 0; }
</style>

<script>
  // ===== このページ専用設定 =====
  const TARGET_SURVEY_ID = "MORI2_TestSurvey_20250531-0608_RO_AM";

  // ★ 共通 assets から GeoJSON を読む（surveys/<name>/ から 2階層上）
  const GEOJSON_URL = "../../assets/mori_survey_github.geojson";

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
      return p.survey_id === surveyId;
    });
    return { ...geojson, features: filtered };
  }

  fetch(GEOJSON_URL)
    .then((r) => {
      if (!r.ok) throw new Error("GeoJSON load failed: " + r.status);
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
          if (p.title) html += "<b>" + p.title + "</b><br>";
          if (p.region) html += "Mesh: " + p.region + "<br>";
          if (p.survey_date) html += "Date: " + p.survey_date + "<br>";
          if (p.survey_id) html += "Survey: " + p.survey_id + "<br>";
          layer.bindPopup(html);
        },
      }).addTo(map);

      if (layer.getBounds().isValid()) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] });
      } else {
        console.warn("No points found for survey_id:", TARGET_SURVEY_ID);
      }
    })
    .catch((e) => console.error(e));
</script>
---

## Suevey id list
| ID | Mesh |
|--------|------|
| [EX-RO-2506-EX_A](./EX-RO-2506-EX_A) | S09W067 |
| [EX-RO-2506-EX_B](./EX-RO-2506-EX_B) | S09W067 |
| [EX-RO-2506-EX_C](./EX-RO-2506-EX_C) | S09W067 |
| [EX-RO-2506-EX_D](./EX-RO-2506-EX_D) | S09W067 |
| [EX-RO-2506-EX_E](./EX-RO-2506-EX_E) | S09W066 |
| [EX-RO-2506-SAF_A](./EX-RO-2506-SAF_A) | S09W067 |
| [EX-RO-2506-SAF_B](./EX-RO-2506-SAF_B) | S09W067 |
| [MA-AM-2506-MAO_H](./MA-AM-2506-MAO_H) | S02W060 |
| [MA-AM-2506-MAO_I](./MA-AM-2506-MAO_I) | S02W060 |
| [MA-AM-2506-MAO_J](./MA-AM-2506-MAO_J) | S02W060 |
| [MA-AM-2506-MAO_K](./MA-AM-2506-MAO_K) | S02W060 |
| [MA-AM-2506-MAO_L](./MA-AM-2506-MAO_L) | S02W060 |
| [MA-AM-2506-MAO_M](./MA-AM-2506-MAO_M) | S02W060 |
| [MA-AM-2506-MAO_N](./MA-AM-2506-MAO_N) | S02W060 |
| [MA-AM-2506-SAF_MAO_A](./MA-AM-2506-SAF_MAO_A) | S02W060 |
| [MA-AM-2506-SAF_MAO_B](./MA-AM-2506-SAF_MAO_B) | S02W060 |
| [PV-RO-2506-PO_F](./PV-RO-2506-PO_F) | S08W065 |
| [PV-RO-2506-PO_G1](./PV-RO-2506-PO_G1) | S08W065 |
| [PV-RO-2506-PO_G2](./PV-RO-2506-PO_G2) | S08W065 |
