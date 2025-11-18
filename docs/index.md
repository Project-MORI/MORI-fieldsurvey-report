# MORI Field Survey Report

**MORI Field Survey Report** is an archive designed to integrate and publish the results of **field surveys conducted under Project MORI**, the JICA–IBAMA technical cooperation initiative.

This website provides a structured, map-linked collection of field observations to support **forest monitoring and enforcement against illegal deforestation** in the Brazilian Amazon.  
Each survey entry follows a standardized format, including:

- Survey location (GeoJSON / map integration)
    
- Background and objectives
    
- Field observations and photographs
    
- Satellite imagery and AI-assisted analysis
    
- Key findings and insights
    

The purpose of this archive is to enhance **transparency**, improve **decision-making support for field operations**, and strengthen **information sharing** among government agencies, researchers, and project stakeholders.

We hope that these efforts contribute to a more sustainable future for the Amazon region.

---

## Survey Map

<div id="map"></div>

<!-- Leaflet & MarkerCluster CSS -->
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet/dist/leaflet.css"
/>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.css"
/>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.Default.css"
/>

<style>
  #map {
    height: 600px;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>

<!-- Leaflet & MarkerCluster JS -->
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster/dist/leaflet.markercluster.js"></script>

<script>
  // トップページから見た GeoJSON の相対パス
  const geojsonUrl = "./assets/MORI_survey_github.geojson";

  // マップ初期化（Amazon全体をざっくり表示）
  const map = L.map("map").setView([-4.5, -62.0], 5);

  // 背景地図（OpenStreetMap）
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // ---- 調査名ごとの色分け用 ----
  const titleColorMap = {};
  const colorPalette = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#a65628",
    "#f781bf",
    "#999999",
  ];

  function getColorForTitle(title) {
    if (!title) {
      return "#3388ff"; // デフォルト色
    }
    if (!titleColorMap[title]) {
      const idx = Object.keys(titleColorMap).length % colorPalette.length;
      titleColorMap[title] = colorPalette[idx];
    }
    return titleColorMap[title];
  }

  // ---- マーカークラスタグループ ----
  const clusterGroup = L.markerClusterGroup();

  // GeoJSON 読み込み
  fetch(geojsonUrl)
    .then((response) => response.json())
    .then((data) => {
      const geojsonLayer = L.geoJSON(data, {
        // ポイントを title ごとの色付き circleMarker に
        pointToLayer: function (feature, latlng) {
          const props = feature.properties || {};
          const title = props.title || props.name || "";
          const color = getColorForTitle(title);

          return L.circleMarker(latlng, {
            radius: 6,
            fillColor: color,
            color: "#000000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.9,
          });
        },

        // ポップアップ（ID をリンクにする・URL未定のため #）
        onEachFeature: function (feature, layer) {
          const p = feature.properties || {};
          const id = p.survey_id || p.id || "";
          const title = p.title || p.name || "";

          // まだ GeoJSON に URL 列がないので暫定的に "#"
          const url = "#";

          let html = "";
          if (title) html += "<b>" + title + "</b><br>";
          if (id) {
            html += 'ID: <a href="' + url + '">' + id + "</a><br>";
          }

          if (html) {
            layer.bindPopup(html);
          }
        },
      });

      // GeoJSON レイヤーをクラスタに追加してマップへ
      clusterGroup.addLayer(geojsonLayer);
      map.addLayer(clusterGroup);

      // すべての点が入るように自動ズーム
      try {
        map.fitBounds(clusterGroup.getBounds());
      } catch (e) {
        console.warn("fitBounds failed:", e);
      }
    })
    .catch((err) => {
      console.error("Failed to load GeoJSON:", err);
    });
</script>


## 調査名の一覧
<!-- BEGIN: AUTO_SURVEY_LIST -->
<ul>
  <li><a href="surveys/FieldSurvey_20211018-19_RO/">FieldSurvey_20211018-19_RO</a></li>
  <li><a href="surveys/FieldSurvey_20220214-21_PA/">FieldSurvey_20220214-21_PA</a></li>
  <li><a href="surveys/FieldSurvey_20220919-23_RO/">FieldSurvey_20220919-23_RO</a></li>
  <li><a href="surveys/FieldSurvey_20230525-0601_RO_AC/">FieldSurvey_20230525-0601_RO_AC</a></li>
  <li><a href="surveys/FIeldSurvey_20231008-14_PA/">FIeldSurvey_20231008-14_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240205-06_PA/">FieldSurvey_20240205-06_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240318-21_PA/">FieldSurvey_20240318-21_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240610-14_PA/">FieldSurvey_20240610-14_PA</a></li>
  <li><a href="surveys/FieldSurvey_20241007-11_RO_AM/">FieldSurvey_20241007-11_RO_AM</a></li>
  <li><a href="surveys/FieldSurvey_20241023-27_PA/">FieldSurvey_20241023-27_PA</a></li>
  <li><a href="surveys/FieldSurvey_20250309-15_RO_AC/">FieldSurvey_20250309-15_RO_AC</a></li>
  <li><a href="surveys/FieldSurvey_20251006-16_PA/">FieldSurvey_20251006-16_PA</a></li>
  <li><a href="surveys/MORI2_TestSurvey_20250531-0608_RO_AM/">MORI2_TestSurvey_20250531-0608_RO_AM</a></li>
</ul>
<!-- END: AUTO_SURVEY_LIST -->
