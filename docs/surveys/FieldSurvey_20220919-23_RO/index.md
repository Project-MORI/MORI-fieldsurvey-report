---
title: FieldSurvey_20220919-23_RO
---

# FieldSurvey_20220919-23_RO

- **Survey Date**: 19/09/2022 - 23/09/2022
- **Member**: IBAMA: 3 / JICA: 3 / JAXA: 3 / AIST: 3
- **Map**: 
![[FieldSurvey_20220919-23_RO.png]]

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
  const TARGET_SURVEY_ID = "FieldSurvey_20220919-23_RO";

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
| [PV-RO-2209-03](./PV-RO-2209-03) | S08W064 |
| [PV-RO-2209-04](./PV-RO-2209-04) | S07W064 |
| [PV-RO-2209-04-2](./PV-RO-2209-04-2) | S07W064 |
| [PV-RO-2209-04-3](./PV-RO-2209-04-3) | S07W064 |
| [PV-RO-2209-05a](./PV-RO-2209-05a) | S08W065 |
| [PV-RO-2209-05b](./PV-RO-2209-05b) | S08W065 |
| [PV-RO-2209-07](./PV-RO-2209-07) | S08W064 |
| [PV-RO-2209-08](./PV-RO-2209-08) | S08W065 |
| [PV-RO-2209-10](./PV-RO-2209-10) | S08W065 |
| [PV-RO-2209-13](./PV-RO-2209-13) | S08W065 |
| [PV-RO-2209-20](./PV-RO-2209-20) | S08W064 |
| [PV-RO-2209-21](./PV-RO-2209-21) | S08W065 |
| [PV-RO-2209-22](./PV-RO-2209-22) | S08W065 |
| [PV-RO-2209-23](./PV-RO-2209-23) | S09W066 |
| [PV-RO-2209-23b](./PV-RO-2209-23b) | S09W066 |
| [PV-RO-2209-24](./PV-RO-2209-24) | S08W066 |
| [PV-RO-2209-25](./PV-RO-2209-25) | S09W067 |
| [PV-RO-2209-26](./PV-RO-2209-26) | S09W067 |
| [PV-RO-2209-27](./PV-RO-2209-27) | S09W067 |
| [PV-RO-2209-28](./PV-RO-2209-28) | S09W067 |
| [PV-RO-2209-29](./PV-RO-2209-29) | S09W066 |
| [PV-RO-2209-30](./PV-RO-2209-30) | S09W066 |
| [PV-RO-2209-31](./PV-RO-2209-31) | S09W066 |
| [PV-RO-2209-32](./PV-RO-2209-32) | S09W066 |
| [PV-RO-2209-33](./PV-RO-2209-33) | S09W067 |
