# Database vs Models Comparison Report
Generated: 2025-12-13 09:51:14

## Summary
- Total Discrepancies: 159
- Critical (High): 4
- Warnings (Medium): 9
- Info (Low): 146

## Critical Issues

- `media_backup`: table_in_db_not_model
- `writers`: table_in_db_not_model
- `media_team`: table_in_db_not_model
- `directors`: table_in_db_not_model

## Warnings

- `tv_channels.metadata`: column_in_db_not_model
- `tv_channels.metadata_`: column_in_model_not_db
- `users_media_affinity.affinity_metadata`: column_in_db_not_model
- `users_media_affinity.affinity_metadata_`: column_in_model_not_db
- `users_sessions.last_activity_at`: column_in_model_not_db
- `staff.staff_type_id`: column_in_db_not_model
- `media_staff.media_id`: column_in_model_not_db
- `notifications.metadata`: column_in_db_not_model
- `notifications._metadata`: column_in_model_not_db
