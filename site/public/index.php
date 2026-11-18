<?php
// Фронт-контроллер. Пока — только главная из seed; маршруты и страницы объектов — задача 8.
require __DIR__ . '/../app/bootstrap.php';
header('Content-Type: text/html; charset=utf-8');
echo pn_render('layout', pn_page_vars());
