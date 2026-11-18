<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('config', fn() => pn_eq(pn_config()['demo'], false, 'по умолчанию не демо'));
