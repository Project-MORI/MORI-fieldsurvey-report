---
title: FieldSurvey_20250309-15_RO_AC
---

# FieldSurvey_20250309-15_RO_AC

- **Survey Date**: 09/03/2025 - 15/03/2025
- **Member**: IBAMA: 3 / JICA: 2
- **Map**: 
![[FieldSurvey_20250309-15_RO_AC.png]]
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
  const TARGET_SURVEY_ID = "FieldSurvey_20250309-15_RO_AC";

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
| [EX-RO-2503-01](./EX-RO-2503-01) | S09W067 |
| [EX-RO-2503-02](./EX-RO-2503-02) | S09W067 |
| [EX-RO-2503-03](./EX-RO-2503-03) | S09W067 |
| [EX-RO-2503-04](./EX-RO-2503-04) | S09W067 |
| [LA-AM-2503-01](./LA-AM-2503-01) | S09W067 |
| [RB-AC-2503-01](./RB-AC-2503-01) | S09W067 |
| [RB-AC-2503-02](./RB-AC-2503-02) | S09W067 |
| [RB-AC-2503-03](./RB-AC-2503-03) | S09W068 |
| [RB-AC-2503-04](./RB-AC-2503-04) | S09W068 |
| [RB-AC-2503-05](./RB-AC-2503-05) | S09W068 |
| [RB-AC-2503-08](./RB-AC-2503-08) | S09W068 |
| [RB-AC-2503-09](./RB-AC-2503-09) | S09W068 |
