-- rendered by Airflow before it is used
SELECT count(*) FROM events
WHERE event_date = '{{ logical_date.strftime("%Y-%m-%d") }}'
  AND loaded_at < '{{ macros.ds_add(ds, 1) }}';
