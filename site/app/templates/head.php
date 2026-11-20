<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><?= $base_tag ?? "" ?><script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width,initial-scale=1">
<?= $seo_head ?>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-6 -6 88 84'%3E%3Crect x='-6' y='-6' width='88' height='84' rx='18' fill='%230E0E0F'/%3E%3Cpath d='M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z' fill='%23F4F2EE'/%3E%3Ccircle cx='67' cy='63' r='9' fill='%23F5553C'/%3E%3C/svg%3E">
<?php if (isset($order)): ?><link rel="preload" as="image" href="assets/img/ekb_dusk.jpg" imagesrcset="assets/img/ekb_dusk-1280.jpg 1280w, assets/img/ekb_dusk-1920.jpg 1920w, assets/img/ekb_dusk.jpg 2880w" imagesizes="100vw" fetchpriority="high"><?php endif; ?>
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<link rel="manifest" href="assets/icons/site.webmanifest">
<?= $jsonld ?>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<link rel="stylesheet" href="assets/css/fx.css">
<script src="assets/js/fx.js" defer></script>
</head>
