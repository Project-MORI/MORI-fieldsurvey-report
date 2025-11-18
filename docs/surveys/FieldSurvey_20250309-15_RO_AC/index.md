---
title: FieldSurvey_20250309-15_RO_AC
---

# FieldSurvey_20250309-15_RO_AC

- **Survey Date**: 
- **Member**: 
- **Map**: 

---

## Suevey id list
| ID | Mesh | Obs. |
|--------|------|------|
| [EX-RO-2503-01](./EX-RO-2503-01) |  |  |
| [EX-RO-2503-02](./EX-RO-2503-02) |  |  |
| [EX-RO-2503-03](./EX-RO-2503-03) |  |  |
| [EX-RO-2503-04](./EX-RO-2503-04) |  |  |
| [LA-AM-2503-01](./LA-AM-2503-01) |  |  |
| [RB-AC-2503-01](./RB-AC-2503-01) |  |  |
| [RB-AC-2503-02](./RB-AC-2503-02) |  |  |
| [RB-AC-2503-03](./RB-AC-2503-03) |  |  |
| [RB-AC-2503-04](./RB-AC-2503-04) |  |  |
| [RB-AC-2503-05](./RB-AC-2503-05) |  |  |
| [RB-AC-2503-08](./RB-AC-2503-08) |  |  |
| [RB-AC-2503-09](./RB-AC-2503-09) |  |  |



## Survey Map

<div id="map"></div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet/dist/leaflet.css"
/>
<style>
  #map {
    height: 600px;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  // トップページから見た GeoJSON の相対パス
  const geojsonUrl = "./assets/MORI_survey_github.geojson";

  const map = L.map("map").setView([-4.5, -62.0], 5); // 適当な初期中心・ズーム

  // 背景地図（OpenStreetMap）
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // GeoJSON 読み込み
  fetch(geojsonUrl)
    .then((response) => response.json())
    .then((data) => {
      const layer = L.geoJSON(data, {
        onEachFeature: function (feature, layer) {
          const p = feature.properties || {};
          const id = p.survey_id || p.id || "";
          const title = p.title || p.name || "";
          const url = p.page_url || ""; // あればページへのリンクに使う

          let html = "";
          if (title) html += "<b>" + title + "</b><br>";
          if (id) html += "ID: " + id + "<br>";
          if (url) html += '<a href="' + url + '">Open survey page</a>';

          if (html) layer.bindPopup(html);
        },
      }).addTo(map);

      // すべての点が入るようにズーム調整
      try {
        map.fitBounds(layer.getBounds());
      } catch (e) {
        console.warn("fitBounds failed:", e);
      }
    })
    .catch((err) => {
      console.error("Failed to load GeoJSON:", err);
    });
</script>