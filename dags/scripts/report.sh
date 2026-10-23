#!/usr/bin/env bash
# Rendered by Airflow as a Jinja template before it runs.
echo "report for {{ logical_date.strftime('%Y-%m-%d') }}"
echo "tomorrow is {{ macros.ds_format(macros.ds_add(ds, 1), '%Y-%m-%d', '%Y%m%d') }}"
