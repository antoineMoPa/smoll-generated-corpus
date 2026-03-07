#!/usr/bin/env python3
"""Creates the level_5 corpus directory structure and all prompts.txt files."""

import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus", "tool_use")

# ---------------------------------------------------------------------------
# Tool domains — each subdomain has tools, schemas, and angles
# Each angle: (filename.corpus, prompt_for_LLM)
# ---------------------------------------------------------------------------

TOOL_DOMAINS = {
    "bash_terminal": {
        "list_files": {
            "tools": "ls | ls_la | ls_lh | ls_R",
            "call_schema": '{ "func_call": "string", "path": "string", "flags": "string" }',
            "response_schema": '{ "entries": ["string"], "count": number }',
            "angles": [
                ("list_files_basic.corpus",
                 "Generate 12 tool-use examples for listing files in a directory with ls. "
                 "Use varied paths (/home/user, /var/log, /etc, /tmp, ~/projects, /usr/bin, /opt). "
                 "Each question should be a natural intent like 'list files in /var/log'."),
                ("list_files_flags.corpus",
                 "Generate 12 tool-use examples for ls with flags (-la, -lh, -R, -a, --sort=size, -lt). "
                 "Use realistic home directories, project folders, and system paths."),
            ],
        },
        "find_files": {
            "tools": "find_by_name | find_by_extension | find_by_size | find_by_date",
            "call_schema": '{ "func_call": "string", "path": "string", "pattern": "string", "type": "string" }',
            "response_schema": '{ "matches": ["string"], "count": number }',
            "angles": [
                ("find_by_name.corpus",
                 "Generate 12 tool-use examples for finding files by name pattern. "
                 "Use realistic file names like *.log, config.yml, *.py, README.md across /home, /etc, /var."),
                ("find_by_extension.corpus",
                 "Generate 12 tool-use examples for finding files by extension (.txt, .conf, .sh, .json, .xml). "
                 "Use varied root paths and include type=file or type=dir distinctions."),
            ],
        },
        "search_text": {
            "tools": "grep_file | grep_recursive | grep_case_insensitive | grep_count",
            "call_schema": '{ "func_call": "string", "pattern": "string", "path": "string", "flags": "string" }',
            "response_schema": '{ "matches": [{ "file": "string", "line": number, "text": "string" }], "count": number }',
            "angles": [
                ("grep_basic.corpus",
                 "Generate 12 tool-use examples for grepping text in files. "
                 "Use realistic search patterns (error, TODO, import, password, hostname) across log files and source code."),
                ("grep_recursive.corpus",
                 "Generate 12 tool-use examples for recursive grep across directories. "
                 "Include -i case-insensitive, -r recursive, -n line numbers. Use /var/log, ~/projects, /etc."),
            ],
        },
        "file_operations": {
            "tools": "copy_file | move_file | delete_file | create_dir",
            "call_schema": '{ "func_call": "string", "source": "string", "destination": "string" }',
            "response_schema": '{ "success": boolean, "message": "string" }',
            "angles": [
                ("copy_move.corpus",
                 "Generate 12 tool-use examples for copying and moving files. "
                 "Use realistic source and destination paths in /home, /tmp, /var/backup. Include backups and renames."),
                ("delete_mkdir.corpus",
                 "Generate 12 tool-use examples for deleting files and creating directories. "
                 "Use realistic temp files, log cleanup scenarios, and project directory creation."),
            ],
        },
        "process_management": {
            "tools": "list_processes | kill_process | get_process_info | top_processes",
            "call_schema": '{ "func_call": "string", "pid": number, "name": "string", "signal": "string" }',
            "response_schema": '{ "processes": [{ "pid": number, "name": "string", "cpu": number, "mem": number }] }',
            "angles": [
                ("list_kill.corpus",
                 "Generate 12 tool-use examples for listing and killing processes. "
                 "Use realistic process names (nginx, python, node, mysql, chrome) and PIDs."),
                ("top_info.corpus",
                 "Generate 12 tool-use examples for getting process info and top CPU/memory consumers. "
                 "Include realistic CPU percentages and memory usage values."),
            ],
        },
        "network_commands": {
            "tools": "curl_get | curl_post | wget_download | ssh_command | ping_host",
            "call_schema": '{ "func_call": "string", "url": "string", "host": "string", "options": "string" }',
            "response_schema": '{ "status_code": number, "output": "string", "elapsed_ms": number }',
            "angles": [
                ("curl_wget.corpus",
                 "Generate 12 tool-use examples for curl GET/POST and wget download operations. "
                 "Use realistic API endpoints, headers, and file downloads from plausible URLs."),
                ("ssh_ping.corpus",
                 "Generate 12 tool-use examples for SSH remote commands and ping host checks. "
                 "Use realistic server hostnames, IPs, and remote commands."),
            ],
        },
        "permissions": {
            "tools": "chmod | chown | check_permissions | add_to_group",
            "call_schema": '{ "func_call": "string", "path": "string", "mode": "string", "owner": "string" }',
            "response_schema": '{ "success": boolean, "previous_mode": "string", "new_mode": "string" }',
            "angles": [
                ("chmod_chown.corpus",
                 "Generate 12 tool-use examples for chmod and chown operations. "
                 "Use realistic file paths, octal modes (755, 644, 600), and user:group combos."),
                ("permissions_check.corpus",
                 "Generate 12 tool-use examples for checking file permissions and adding users to groups. "
                 "Use realistic Unix usernames, groups, and file paths."),
            ],
        },
    },
    "weather_api": {
        "current_conditions": {
            "tools": "get_temperature | get_humidity | get_wind_speed | get_uv_index",
            "call_schema": '{ "func_call": "string", "location": "string", "unit": "celsius|fahrenheit" }',
            "response_schema": '{ "value": number, "unit": "string", "timestamp": "string" }',
            "angles": [
                ("temperature.corpus",
                 "Generate 12 tool-use examples for getting current temperature in various cities worldwide. "
                 "Mix celsius and fahrenheit. Use real city names across different continents."),
                ("humidity_wind.corpus",
                 "Generate 12 tool-use examples for getting current humidity and wind speed. "
                 "Use coastal cities, inland cities, and mountain locations. Use realistic values."),
            ],
        },
        "multi_metric": {
            "tools": "get_current_weather | get_feels_like | get_pressure | get_visibility",
            "call_schema": '{ "func_call": "string", "location": "string", "metrics": ["string"] }',
            "response_schema": '{ "location": "string", "metrics": { "temperature": number, "humidity": number, "pressure": number } }',
            "angles": [
                ("full_conditions.corpus",
                 "Generate 12 tool-use examples for fetching multiple weather metrics at once. "
                 "Use realistic city+country combos and return objects with multiple fields."),
                ("feels_like_pressure.corpus",
                 "Generate 12 tool-use examples for feels-like temperature and barometric pressure. "
                 "Use varied global locations and realistic hPa pressure values."),
            ],
        },
        "forecast": {
            "tools": "get_forecast_daily | get_forecast_hourly | get_forecast_weekly",
            "call_schema": '{ "func_call": "string", "location": "string", "days": number, "unit": "string" }',
            "response_schema": '{ "location": "string", "forecast": [{ "date": "string", "high": number, "low": number, "condition": "string" }] }',
            "angles": [
                ("daily_forecast.corpus",
                 "Generate 12 tool-use examples for 3-7 day weather forecasts. "
                 "Use real cities. Responses should include date, high/low temps, and weather condition strings."),
                ("hourly_forecast.corpus",
                 "Generate 12 tool-use examples for hourly weather forecasts. "
                 "Use realistic time ranges and include precipitation probability."),
            ],
        },
        "alerts": {
            "tools": "get_weather_alerts | get_storm_warnings | get_air_quality_index",
            "call_schema": '{ "func_call": "string", "location": "string", "severity": "string" }',
            "response_schema": '{ "alerts": [{ "type": "string", "severity": "string", "message": "string", "expires": "string" }] }',
            "angles": [
                ("storm_alerts.corpus",
                 "Generate 12 tool-use examples for weather alerts and storm warnings. "
                 "Use coastal storm, tornado, blizzard, and flood scenarios with realistic messages."),
                ("air_quality.corpus",
                 "Generate 12 tool-use examples for air quality index queries. "
                 "Use cities with known pollution issues. Include AQI values and health recommendations."),
            ],
        },
    },
    "cloud_server_api": {
        "instance_lifecycle": {
            "tools": "start_instance | stop_instance | restart_instance | terminate_instance",
            "call_schema": '{ "func_call": "string", "instance_id": "string", "region": "string" }',
            "response_schema": '{ "instance_id": "string", "state": "string", "message": "string" }',
            "angles": [
                ("start_stop.corpus",
                 "Generate 12 tool-use examples for starting and stopping cloud instances. "
                 "Use realistic instance IDs (i-xxxxxxxx style), regions (us-east-1, eu-west-2, ap-southeast-1)."),
                ("restart_terminate.corpus",
                 "Generate 12 tool-use examples for restarting and terminating cloud instances. "
                 "Include scenarios like scheduled maintenance and scale-down events."),
            ],
        },
        "instance_status": {
            "tools": "get_instance_status | list_instances | get_instance_metrics",
            "call_schema": '{ "func_call": "string", "instance_id": "string", "region": "string", "filter": "string" }',
            "response_schema": '{ "instances": [{ "id": "string", "type": "string", "state": "string", "ip": "string" }] }',
            "angles": [
                ("status_list.corpus",
                 "Generate 12 tool-use examples for checking instance status and listing running instances. "
                 "Use realistic instance types (t3.medium, m5.large, c5.xlarge) and states."),
                ("metrics.corpus",
                 "Generate 12 tool-use examples for getting CPU, memory, and network metrics for instances. "
                 "Return realistic percentage and throughput values."),
            ],
        },
        "scaling_operations": {
            "tools": "scale_out | scale_in | set_auto_scaling | get_scaling_policy",
            "call_schema": '{ "func_call": "string", "group_id": "string", "min_size": number, "max_size": number, "desired": number }',
            "response_schema": '{ "group_id": "string", "current_capacity": number, "status": "string" }',
            "angles": [
                ("scale_out_in.corpus",
                 "Generate 12 tool-use examples for scaling cloud instance groups out and in. "
                 "Use realistic auto-scaling group names and capacity numbers."),
                ("auto_scaling_policy.corpus",
                 "Generate 12 tool-use examples for setting and getting auto-scaling policies. "
                 "Include CPU threshold triggers and cooldown periods."),
            ],
        },
        "storage_volumes": {
            "tools": "create_volume | attach_volume | detach_volume | snapshot_volume | list_volumes",
            "call_schema": '{ "func_call": "string", "volume_id": "string", "instance_id": "string", "size_gb": number }',
            "response_schema": '{ "volume_id": "string", "size_gb": number, "state": "string", "attached_to": "string" }',
            "angles": [
                ("create_attach.corpus",
                 "Generate 12 tool-use examples for creating and attaching storage volumes. "
                 "Use realistic sizes (50GB, 200GB, 1TB) and instance IDs."),
                ("snapshot_list.corpus",
                 "Generate 12 tool-use examples for snapshotting and listing volumes. "
                 "Include backup scenarios and volume state transitions."),
            ],
        },
    },
    "smart_home": {
        "garage_door": {
            "tools": "open_garage | close_garage | get_garage_status | set_garage_timer",
            "call_schema": '{ "func_call": "string", "door_id": "string", "delay_seconds": number }',
            "response_schema": '{ "door_id": "string", "state": "open|closed|opening|closing", "timestamp": "string" }',
            "angles": [
                ("open_close.corpus",
                 "Generate 12 tool-use examples for opening and closing a smart garage door. "
                 "Use varied door IDs and scenarios like arriving home or leaving for work."),
                ("status_timer.corpus",
                 "Generate 12 tool-use examples for checking garage door status and setting auto-close timers. "
                 "Use realistic delay values and status checks."),
            ],
        },
        "thermostat": {
            "tools": "set_temperature | get_temperature | set_mode | get_schedule",
            "call_schema": '{ "func_call": "string", "device_id": "string", "temperature": number, "mode": "heat|cool|auto|off" }',
            "response_schema": '{ "device_id": "string", "current_temp": number, "target_temp": number, "mode": "string" }',
            "angles": [
                ("set_get_temp.corpus",
                 "Generate 12 tool-use examples for setting and getting thermostat temperature. "
                 "Use realistic home temperatures (18-26°C) and scenarios like going to bed or leaving home."),
                ("mode_schedule.corpus",
                 "Generate 12 tool-use examples for setting thermostat mode and checking schedules. "
                 "Include heat, cool, auto, and off modes with time-based scenarios."),
            ],
        },
        "smart_lighting": {
            "tools": "turn_on_light | turn_off_light | set_brightness | set_color | get_light_status",
            "call_schema": '{ "func_call": "string", "light_id": "string", "brightness": number, "color": "string" }',
            "response_schema": '{ "light_id": "string", "state": "on|off", "brightness": number, "color": "string" }',
            "angles": [
                ("on_off_brightness.corpus",
                 "Generate 12 tool-use examples for turning lights on/off and adjusting brightness. "
                 "Use room names (living_room, bedroom, kitchen) and percentage brightness values."),
                ("color_status.corpus",
                 "Generate 12 tool-use examples for setting light colors and checking status. "
                 "Use color names (warm white, blue, sunset orange) and hex values."),
            ],
        },
        "door_locks": {
            "tools": "lock_door | unlock_door | get_lock_status | set_access_code",
            "call_schema": '{ "func_call": "string", "lock_id": "string", "user_id": "string", "code": "string" }',
            "response_schema": '{ "lock_id": "string", "state": "locked|unlocked", "last_action_by": "string", "timestamp": "string" }',
            "angles": [
                ("lock_unlock.corpus",
                 "Generate 12 tool-use examples for locking and unlocking smart door locks. "
                 "Use front_door, back_door, garage scenarios with user IDs."),
                ("access_code.corpus",
                 "Generate 12 tool-use examples for setting access codes and checking lock status. "
                 "Include temporary codes for guests and status history."),
            ],
        },
    },
    "coffee_machine": {
        "brewing": {
            "tools": "brew_coffee | brew_espresso | brew_latte | brew_cappuccino",
            "call_schema": '{ "func_call": "string", "size": "small|medium|large", "strength": "mild|medium|strong", "milk": "string" }',
            "response_schema": '{ "order_id": "string", "status": "string", "estimated_seconds": number }',
            "angles": [
                ("espresso_latte.corpus",
                 "Generate 12 tool-use examples for brewing espresso and latte. "
                 "Vary size (small/medium/large), strength (mild/medium/strong), and milk type (oat, almond, whole)."),
                ("drip_cappuccino.corpus",
                 "Generate 12 tool-use examples for brewing drip coffee and cappuccino. "
                 "Include morning rush, office scenarios. Vary cup sizes and temperatures."),
            ],
        },
        "settings": {
            "tools": "set_temperature | set_grind_level | set_brew_time | get_current_settings",
            "call_schema": '{ "func_call": "string", "parameter": "string", "value": "string" }',
            "response_schema": '{ "parameter": "string", "previous_value": "string", "new_value": "string" }',
            "angles": [
                ("temperature_grind.corpus",
                 "Generate 12 tool-use examples for adjusting coffee machine temperature and grind level. "
                 "Use realistic temp ranges (88-96°C) and grind settings (1-10 scale)."),
                ("brew_time_settings.corpus",
                 "Generate 12 tool-use examples for setting brew time and retrieving current settings. "
                 "Use realistic brew durations and settings objects."),
            ],
        },
        "maintenance": {
            "tools": "clean_machine | descale | check_water_level | check_bean_level | empty_grounds",
            "call_schema": '{ "func_call": "string", "machine_id": "string" }',
            "response_schema": '{ "machine_id": "string", "status": "string", "water_level_pct": number, "bean_level_pct": number }',
            "angles": [
                ("clean_descale.corpus",
                 "Generate 12 tool-use examples for cleaning and descaling a coffee machine. "
                 "Include routine maintenance, scale buildup alerts, and completion confirmations."),
                ("levels_grounds.corpus",
                 "Generate 12 tool-use examples for checking water/bean levels and emptying the grounds bin. "
                 "Use realistic percentage values and maintenance reminders."),
            ],
        },
    },
    "vending_machine": {
        "purchase": {
            "tools": "purchase_item | get_item_info | check_availability",
            "call_schema": '{ "func_call": "string", "slot_id": "string", "quantity": number }',
            "response_schema": '{ "slot_id": "string", "item_name": "string", "price": number, "status": "string" }',
            "angles": [
                ("buy_snacks.corpus",
                 "Generate 12 tool-use examples for purchasing snacks and drinks from a vending machine. "
                 "Use slot IDs (A1-D9), realistic product names, and prices."),
                ("check_availability.corpus",
                 "Generate 12 tool-use examples for checking item availability before purchase. "
                 "Include out-of-stock and low-stock scenarios."),
            ],
        },
        "inventory": {
            "tools": "list_inventory | restock_item | get_low_stock | update_price",
            "call_schema": '{ "func_call": "string", "slot_id": "string", "quantity": number, "price": number }',
            "response_schema": '{ "inventory": [{ "slot_id": "string", "name": "string", "quantity": number, "price": number }] }',
            "angles": [
                ("list_restock.corpus",
                 "Generate 12 tool-use examples for listing inventory and restocking items. "
                 "Use a realistic 4×9 slot grid with snacks, drinks, and candy."),
                ("low_stock_price.corpus",
                 "Generate 12 tool-use examples for getting low-stock alerts and updating prices. "
                 "Use realistic reorder thresholds and price adjustment scenarios."),
            ],
        },
        "payment": {
            "tools": "process_cash | process_card | process_mobile_pay | get_change | refund_transaction",
            "call_schema": '{ "func_call": "string", "amount": number, "currency": "string", "transaction_id": "string" }',
            "response_schema": '{ "transaction_id": "string", "status": "string", "change": number, "receipt": "string" }',
            "angles": [
                ("cash_card.corpus",
                 "Generate 12 tool-use examples for cash and card payment processing in a vending machine. "
                 "Use realistic prices, amounts tendered, and change calculations."),
                ("mobile_refund.corpus",
                 "Generate 12 tool-use examples for mobile payment (Apple Pay, Google Pay) and refund processing. "
                 "Include failed transaction and refund scenarios."),
            ],
        },
    },
    "crm": {
        "contact_lookup": {
            "tools": "search_contact | get_contact_by_id | find_contacts_by_company | find_contacts_by_tag",
            "call_schema": '{ "func_call": "string", "query": "string", "field": "string", "limit": number }',
            "response_schema": '{ "contacts": [{ "id": "string", "name": "string", "email": "string", "company": "string", "phone": "string" }], "total": number }',
            "angles": [
                ("search_by_name_email.corpus",
                 "Generate 12 tool-use examples for searching CRM contacts by name and email. "
                 "Use realistic full names, company names, and email addresses."),
                ("search_by_company_tag.corpus",
                 "Generate 12 tool-use examples for finding contacts by company or tag. "
                 "Use B2B company names and CRM tags (enterprise, prospect, churned, VIP)."),
            ],
        },
        "contact_management": {
            "tools": "create_contact | update_contact | delete_contact | add_note | add_tag",
            "call_schema": '{ "func_call": "string", "contact_id": "string", "name": "string", "email": "string", "company": "string", "note": "string" }',
            "response_schema": '{ "contact_id": "string", "status": "string", "updated_fields": ["string"] }',
            "angles": [
                ("create_update.corpus",
                 "Generate 12 tool-use examples for creating and updating CRM contacts. "
                 "Use realistic contact details, job titles, and company names."),
                ("notes_tags.corpus",
                 "Generate 12 tool-use examples for adding notes and tags to contacts. "
                 "Use realistic sales notes (follow-up calls, meeting summaries) and pipeline tags."),
            ],
        },
        "deal_pipeline": {
            "tools": "create_deal | update_deal_stage | get_deal | list_deals_by_stage | close_deal",
            "call_schema": '{ "func_call": "string", "deal_id": "string", "contact_id": "string", "stage": "string", "value": number }',
            "response_schema": '{ "deal_id": "string", "name": "string", "stage": "string", "value": number, "probability": number }',
            "angles": [
                ("create_update_deal.corpus",
                 "Generate 12 tool-use examples for creating and updating sales deals. "
                 "Use pipeline stages (prospect, qualified, proposal, negotiation, closed_won, closed_lost)."),
                ("list_close_deal.corpus",
                 "Generate 12 tool-use examples for listing deals by stage and closing deals. "
                 "Use realistic deal values ($5k–$500k) and win/loss reasons."),
            ],
        },
        "reporting": {
            "tools": "get_sales_report | get_conversion_rate | get_pipeline_summary | get_activity_report",
            "call_schema": '{ "func_call": "string", "period": "string", "group_by": "string", "filters": "string" }',
            "response_schema": '{ "period": "string", "total_value": number, "deal_count": number, "conversion_rate": number }',
            "angles": [
                ("sales_report.corpus",
                 "Generate 12 tool-use examples for generating CRM sales reports. "
                 "Use monthly, quarterly, and annual periods. Return realistic revenue numbers."),
                ("pipeline_activity.corpus",
                 "Generate 12 tool-use examples for pipeline summaries and activity reports. "
                 "Include calls made, emails sent, meetings booked per rep."),
            ],
        },
    },
    "calendar": {
        "create_events": {
            "tools": "create_event | create_recurring_event | create_all_day_event",
            "call_schema": '{ "func_call": "string", "title": "string", "start": "string", "end": "string", "location": "string", "description": "string" }',
            "response_schema": '{ "event_id": "string", "title": "string", "start": "string", "end": "string", "calendar": "string" }',
            "angles": [
                ("meetings_appointments.corpus",
                 "Generate 12 tool-use examples for creating calendar events like meetings and appointments. "
                 "Use realistic event titles, ISO 8601 times, and office/video call locations."),
                ("recurring_all_day.corpus",
                 "Generate 12 tool-use examples for recurring and all-day events. "
                 "Include weekly stand-ups, monthly reviews, birthdays, and holidays."),
            ],
        },
        "availability": {
            "tools": "check_availability | find_free_slot | get_busy_times | block_time",
            "call_schema": '{ "func_call": "string", "user_id": "string", "date": "string", "duration_minutes": number }',
            "response_schema": '{ "available": boolean, "free_slots": [{ "start": "string", "end": "string" }] }',
            "angles": [
                ("check_free_slot.corpus",
                 "Generate 12 tool-use examples for checking calendar availability and finding free slots. "
                 "Use realistic work hours (9-17), durations (30min, 1h, 2h), and date ranges."),
                ("busy_block.corpus",
                 "Generate 12 tool-use examples for getting busy times and blocking calendar time. "
                 "Include focus time blocks and travel buffer scenarios."),
            ],
        },
        "invites_reminders": {
            "tools": "send_invite | accept_invite | decline_invite | set_reminder | get_rsvp_status",
            "call_schema": '{ "func_call": "string", "event_id": "string", "attendee_email": "string", "reminder_minutes": number }',
            "response_schema": '{ "event_id": "string", "status": "string", "attendees": [{ "email": "string", "rsvp": "string" }] }',
            "angles": [
                ("invite_rsvp.corpus",
                 "Generate 12 tool-use examples for sending calendar invites and tracking RSVPs. "
                 "Use realistic attendee emails and meeting scenarios."),
                ("reminders.corpus",
                 "Generate 12 tool-use examples for setting event reminders. "
                 "Use varied lead times (5min, 15min, 1h, 1d) and reminder methods (email, push, sms)."),
            ],
        },
    },
    "ecommerce": {
        "product_search": {
            "tools": "search_products | filter_products | get_product_details | get_recommendations",
            "call_schema": '{ "func_call": "string", "query": "string", "category": "string", "min_price": number, "max_price": number, "sort_by": "string" }',
            "response_schema": '{ "products": [{ "id": "string", "name": "string", "price": number, "rating": number, "in_stock": boolean }], "total": number }',
            "angles": [
                ("search_filter.corpus",
                 "Generate 12 tool-use examples for searching and filtering products. "
                 "Use electronics, clothing, books, and home goods categories. Vary price ranges."),
                ("details_recommendations.corpus",
                 "Generate 12 tool-use examples for getting product details and recommendations. "
                 "Include realistic product names, SKUs, and related product suggestions."),
            ],
        },
        "cart_checkout": {
            "tools": "add_to_cart | remove_from_cart | update_quantity | get_cart | apply_coupon | checkout",
            "call_schema": '{ "func_call": "string", "product_id": "string", "quantity": number, "coupon_code": "string" }',
            "response_schema": '{ "cart_id": "string", "items": [{ "product_id": "string", "name": "string", "quantity": number, "price": number }], "total": number }',
            "angles": [
                ("add_remove_cart.corpus",
                 "Generate 12 tool-use examples for adding and removing items from a shopping cart. "
                 "Use realistic product IDs and quantities."),
                ("coupon_checkout.corpus",
                 "Generate 12 tool-use examples for applying coupons and completing checkout. "
                 "Include discount codes, invalid coupons, and order totals."),
            ],
        },
        "order_tracking": {
            "tools": "get_order_status | track_shipment | get_order_history | cancel_order",
            "call_schema": '{ "func_call": "string", "order_id": "string", "tracking_number": "string" }',
            "response_schema": '{ "order_id": "string", "status": "string", "estimated_delivery": "string", "tracking_events": [{ "date": "string", "location": "string", "status": "string" }] }',
            "angles": [
                ("track_status.corpus",
                 "Generate 12 tool-use examples for tracking orders and checking shipment status. "
                 "Use realistic order IDs and tracking event sequences (picked up, in transit, delivered)."),
                ("history_cancel.corpus",
                 "Generate 12 tool-use examples for viewing order history and cancelling orders. "
                 "Include various cancellation reasons and refund status."),
            ],
        },
        "returns": {
            "tools": "initiate_return | get_return_status | exchange_item | get_refund_status",
            "call_schema": '{ "func_call": "string", "order_id": "string", "item_id": "string", "reason": "string" }',
            "response_schema": '{ "return_id": "string", "status": "string", "refund_amount": number, "label_url": "string" }',
            "angles": [
                ("initiate_return.corpus",
                 "Generate 12 tool-use examples for initiating product returns. "
                 "Use reasons like defective, wrong size, not as described. Include return label generation."),
                ("exchange_refund.corpus",
                 "Generate 12 tool-use examples for item exchanges and refund status checks. "
                 "Include full and partial refund scenarios."),
            ],
        },
    },
    "database": {
        "select_query": {
            "tools": "select_records | select_with_filter | select_with_join | count_records",
            "call_schema": '{ "func_call": "string", "table": "string", "columns": ["string"], "where": "string", "limit": number }',
            "response_schema": '{ "rows": [{}], "count": number, "query_ms": number }',
            "angles": [
                ("basic_select.corpus",
                 "Generate 12 tool-use examples for basic SELECT queries on tables like users, orders, products. "
                 "Use realistic column names and WHERE conditions."),
                ("join_count.corpus",
                 "Generate 12 tool-use examples for JOIN queries and record counting. "
                 "Use realistic multi-table schemas (users, orders, products, inventory)."),
            ],
        },
        "insert_record": {
            "tools": "insert_record | bulk_insert | insert_and_return",
            "call_schema": '{ "func_call": "string", "table": "string", "data": {} }',
            "response_schema": '{ "id": number, "table": "string", "inserted": number, "status": "string" }',
            "angles": [
                ("insert_user_order.corpus",
                 "Generate 12 tool-use examples for inserting new records into users and orders tables. "
                 "Use realistic field names and values."),
                ("bulk_insert.corpus",
                 "Generate 12 tool-use examples for bulk inserting multiple records. "
                 "Use product catalogs, event logs, and batch user imports."),
            ],
        },
        "update_record": {
            "tools": "update_record | update_batch | soft_delete | restore_record",
            "call_schema": '{ "func_call": "string", "table": "string", "id": number, "data": {}, "where": "string" }',
            "response_schema": '{ "affected_rows": number, "status": "string", "updated_at": "string" }',
            "angles": [
                ("update_single.corpus",
                 "Generate 12 tool-use examples for updating single records by ID. "
                 "Use user profile updates, order status changes, and price modifications."),
                ("batch_soft_delete.corpus",
                 "Generate 12 tool-use examples for batch updates and soft deletes. "
                 "Include deactivating users, archiving orders, and restoring deleted records."),
            ],
        },
        "aggregate": {
            "tools": "sum_column | avg_column | group_by_query | min_max_query",
            "call_schema": '{ "func_call": "string", "table": "string", "column": "string", "group_by": "string", "where": "string" }',
            "response_schema": '{ "result": number, "groups": [{ "key": "string", "value": number }] }',
            "angles": [
                ("sum_avg.corpus",
                 "Generate 12 tool-use examples for SUM and AVG aggregations. "
                 "Use orders total, product prices, session durations. Return realistic numbers."),
                ("group_minmax.corpus",
                 "Generate 12 tool-use examples for GROUP BY and MIN/MAX queries. "
                 "Include sales by region, top products, and date range queries."),
            ],
        },
    },
    "music_player": {
        "playback_control": {
            "tools": "play | pause | stop | skip_next | skip_previous | seek",
            "call_schema": '{ "func_call": "string", "track_id": "string", "position_seconds": number }',
            "response_schema": '{ "track_id": "string", "title": "string", "artist": "string", "state": "playing|paused|stopped", "position_seconds": number }',
            "angles": [
                ("play_pause_skip.corpus",
                 "Generate 12 tool-use examples for play, pause, and skip controls. "
                 "Use real-sounding song titles, artist names, and track IDs."),
                ("stop_seek.corpus",
                 "Generate 12 tool-use examples for stopping playback and seeking to position. "
                 "Use realistic track lengths and seek positions."),
            ],
        },
        "volume_settings": {
            "tools": "set_volume | get_volume | mute | unmute | set_equalizer",
            "call_schema": '{ "func_call": "string", "level": number, "preset": "string" }',
            "response_schema": '{ "volume": number, "muted": boolean, "equalizer_preset": "string" }',
            "angles": [
                ("volume_mute.corpus",
                 "Generate 12 tool-use examples for setting volume and muting/unmuting. "
                 "Use 0-100 volume scale and contextual scenarios (night mode, party mode)."),
                ("equalizer.corpus",
                 "Generate 12 tool-use examples for setting equalizer presets. "
                 "Use genres (rock, jazz, classical, bass boost, podcast) as preset names."),
            ],
        },
        "search_browse": {
            "tools": "search_tracks | search_artist | search_album | get_trending | get_genre_playlist",
            "call_schema": '{ "func_call": "string", "query": "string", "limit": number, "genre": "string" }',
            "response_schema": '{ "results": [{ "id": "string", "title": "string", "artist": "string", "duration_seconds": number }], "total": number }',
            "angles": [
                ("search_tracks_artist.corpus",
                 "Generate 12 tool-use examples for searching tracks and artists. "
                 "Use plausible song titles and artist names across genres."),
                ("trending_genre.corpus",
                 "Generate 12 tool-use examples for browsing trending music and genre playlists. "
                 "Include pop, hip-hop, classical, electronic, and jazz genres."),
            ],
        },
        "playlist_management": {
            "tools": "create_playlist | add_to_playlist | remove_from_playlist | delete_playlist | list_playlists",
            "call_schema": '{ "func_call": "string", "playlist_id": "string", "name": "string", "track_id": "string" }',
            "response_schema": '{ "playlist_id": "string", "name": "string", "track_count": number, "duration_seconds": number }',
            "angles": [
                ("create_add.corpus",
                 "Generate 12 tool-use examples for creating playlists and adding tracks. "
                 "Use creative playlist names (Morning Run, Study Session, Friday Night)."),
                ("remove_delete_list.corpus",
                 "Generate 12 tool-use examples for removing tracks and deleting/listing playlists. "
                 "Include various playlist management scenarios."),
            ],
        },
    },
    "email": {
        "send_compose": {
            "tools": "send_email | compose_draft | send_reply | forward_email",
            "call_schema": '{ "func_call": "string", "to": ["string"], "cc": ["string"], "subject": "string", "body": "string", "attachments": ["string"] }',
            "response_schema": '{ "message_id": "string", "status": "sent|draft|failed", "timestamp": "string" }',
            "angles": [
                ("send_reply.corpus",
                 "Generate 12 tool-use examples for sending emails and replies. "
                 "Use realistic subject lines, recipient addresses, and short body text."),
                ("draft_forward.corpus",
                 "Generate 12 tool-use examples for composing drafts and forwarding emails. "
                 "Include business, personal, and team communication scenarios."),
            ],
        },
        "read_inbox": {
            "tools": "get_inbox | get_email | mark_as_read | mark_as_unread | get_unread_count",
            "call_schema": '{ "func_call": "string", "folder": "string", "message_id": "string", "limit": number }',
            "response_schema": '{ "messages": [{ "id": "string", "from": "string", "subject": "string", "date": "string", "read": boolean }], "total": number }',
            "angles": [
                ("read_inbox.corpus",
                 "Generate 12 tool-use examples for reading inbox and fetching email content. "
                 "Use realistic sender addresses, subjects, and inbox states."),
                ("mark_read_count.corpus",
                 "Generate 12 tool-use examples for marking emails read/unread and counting unread messages. "
                 "Include various folder contexts (inbox, work, newsletters)."),
            ],
        },
        "search_filter": {
            "tools": "search_emails | filter_by_sender | filter_by_date | filter_by_label",
            "call_schema": '{ "func_call": "string", "query": "string", "from": "string", "after": "string", "before": "string", "label": "string" }',
            "response_schema": '{ "messages": [{ "id": "string", "from": "string", "subject": "string", "date": "string" }], "count": number }',
            "angles": [
                ("search_by_keyword.corpus",
                 "Generate 12 tool-use examples for searching emails by keyword and sender. "
                 "Use realistic search terms (invoice, meeting, password reset, order confirmation)."),
                ("filter_date_label.corpus",
                 "Generate 12 tool-use examples for filtering emails by date range and label. "
                 "Use labels like work, personal, newsletters, urgent."),
            ],
        },
        "manage_organize": {
            "tools": "move_to_folder | create_label | delete_email | archive_email | unsubscribe",
            "call_schema": '{ "func_call": "string", "message_id": "string", "folder": "string", "label": "string" }',
            "response_schema": '{ "message_id": "string", "action": "string", "status": "string" }',
            "angles": [
                ("move_label.corpus",
                 "Generate 12 tool-use examples for moving emails to folders and adding labels. "
                 "Use realistic folder names and label categorization."),
                ("delete_archive.corpus",
                 "Generate 12 tool-use examples for deleting, archiving, and unsubscribing from emails. "
                 "Include bulk operations and newsletter management."),
            ],
        },
    },
    "banking": {
        "account_balance": {
            "tools": "get_balance | get_account_summary | get_available_credit | get_account_details",
            "call_schema": '{ "func_call": "string", "account_id": "string", "account_type": "checking|savings|credit" }',
            "response_schema": '{ "account_id": "string", "balance": number, "currency": "string", "available": number }',
            "angles": [
                ("checking_savings.corpus",
                 "Generate 12 tool-use examples for checking account balances. "
                 "Use realistic account IDs and balances across checking, savings, and credit accounts."),
                ("credit_summary.corpus",
                 "Generate 12 tool-use examples for credit limit and account summary queries. "
                 "Include available credit, statement balance, and minimum payment due."),
            ],
        },
        "transfers": {
            "tools": "transfer_funds | schedule_transfer | cancel_transfer | get_transfer_status",
            "call_schema": '{ "func_call": "string", "from_account": "string", "to_account": "string", "amount": number, "currency": "string", "scheduled_date": "string" }',
            "response_schema": '{ "transfer_id": "string", "status": "string", "amount": number, "estimated_arrival": "string" }',
            "angles": [
                ("immediate_transfer.corpus",
                 "Generate 12 tool-use examples for immediate fund transfers. "
                 "Use realistic account numbers, USD/EUR/GBP amounts, and transfer reasons."),
                ("scheduled_cancel.corpus",
                 "Generate 12 tool-use examples for scheduling and cancelling transfers. "
                 "Include bill payment, rent, and recurring transfer scenarios."),
            ],
        },
        "transaction_history": {
            "tools": "get_transactions | get_transaction_by_id | get_statements | search_transactions",
            "call_schema": '{ "func_call": "string", "account_id": "string", "from_date": "string", "to_date": "string", "limit": number }',
            "response_schema": '{ "transactions": [{ "id": "string", "date": "string", "description": "string", "amount": number, "type": "debit|credit" }], "total": number }',
            "angles": [
                ("recent_transactions.corpus",
                 "Generate 12 tool-use examples for fetching recent transaction history. "
                 "Use realistic merchant names, amounts, and debit/credit types."),
                ("search_statements.corpus",
                 "Generate 12 tool-use examples for searching transactions and downloading statements. "
                 "Include date range queries and merchant search."),
            ],
        },
        "currency_exchange": {
            "tools": "get_exchange_rate | convert_currency | buy_foreign_currency | get_supported_currencies",
            "call_schema": '{ "func_call": "string", "from_currency": "string", "to_currency": "string", "amount": number }',
            "response_schema": '{ "from": "string", "to": "string", "rate": number, "converted_amount": number, "fee": number }',
            "angles": [
                ("exchange_rates.corpus",
                 "Generate 12 tool-use examples for getting currency exchange rates. "
                 "Use major currency pairs (USD/EUR, GBP/JPY, EUR/CHF) with realistic rates."),
                ("convert_buy.corpus",
                 "Generate 12 tool-use examples for converting currency and buying foreign currency. "
                 "Include travel and international wire transfer scenarios."),
            ],
        },
    },
    "food_ordering": {
        "restaurant_search": {
            "tools": "search_restaurants | filter_by_cuisine | get_restaurant_menu | get_restaurant_details",
            "call_schema": '{ "func_call": "string", "location": "string", "cuisine": "string", "max_delivery_time": number, "min_rating": number }',
            "response_schema": '{ "restaurants": [{ "id": "string", "name": "string", "cuisine": "string", "rating": number, "delivery_time_min": number }], "total": number }',
            "angles": [
                ("search_filter.corpus",
                 "Generate 12 tool-use examples for searching and filtering restaurants. "
                 "Use cities, cuisine types (Italian, Thai, Mexican, Indian), and rating filters."),
                ("menu_details.corpus",
                 "Generate 12 tool-use examples for getting restaurant menus and details. "
                 "Include realistic restaurant names, menu items, and prices."),
            ],
        },
        "place_order": {
            "tools": "add_item_to_order | remove_item | apply_promo | place_order | get_order_estimate",
            "call_schema": '{ "func_call": "string", "restaurant_id": "string", "item_id": "string", "quantity": number, "special_instructions": "string" }',
            "response_schema": '{ "order_id": "string", "items": [{ "name": "string", "quantity": number, "price": number }], "total": number, "estimated_delivery_min": number }',
            "angles": [
                ("add_items.corpus",
                 "Generate 12 tool-use examples for adding food items to an order. "
                 "Use realistic dish names, quantities, and special instructions (no onions, extra sauce)."),
                ("promo_place.corpus",
                 "Generate 12 tool-use examples for applying promo codes and placing orders. "
                 "Include discount codes, free delivery promos, and order confirmation."),
            ],
        },
        "track_order": {
            "tools": "track_delivery | get_order_status | contact_driver | rate_order",
            "call_schema": '{ "func_call": "string", "order_id": "string" }',
            "response_schema": '{ "order_id": "string", "status": "string", "driver_name": "string", "eta_minutes": number, "location": "string" }',
            "angles": [
                ("track_status.corpus",
                 "Generate 12 tool-use examples for tracking food delivery and checking order status. "
                 "Use status stages (preparing, picked up, on the way, delivered) with ETA values."),
                ("rate_contact.corpus",
                 "Generate 12 tool-use examples for rating completed orders and contacting the driver. "
                 "Include 1-5 star ratings and review comments."),
            ],
        },
    },
    "iot_sensors": {
        "sensor_readings": {
            "tools": "get_sensor_reading | get_all_sensors | get_sensor_by_location | get_sensor_battery",
            "call_schema": '{ "func_call": "string", "sensor_id": "string", "location": "string", "type": "temperature|humidity|motion|co2|light" }',
            "response_schema": '{ "sensor_id": "string", "type": "string", "value": number, "unit": "string", "timestamp": "string", "battery_pct": number }',
            "angles": [
                ("temperature_humidity.corpus",
                 "Generate 12 tool-use examples for reading temperature and humidity sensors. "
                 "Use room/location names and realistic sensor values with units."),
                ("motion_co2_light.corpus",
                 "Generate 12 tool-use examples for motion, CO2, and light level sensor readings. "
                 "Use office and home locations with realistic environmental values."),
            ],
        },
        "alert_configuration": {
            "tools": "set_alert_threshold | get_alerts | acknowledge_alert | disable_alert",
            "call_schema": '{ "func_call": "string", "sensor_id": "string", "metric": "string", "threshold": number, "condition": "above|below" }',
            "response_schema": '{ "alert_id": "string", "sensor_id": "string", "status": "string", "threshold": number }',
            "angles": [
                ("set_threshold.corpus",
                 "Generate 12 tool-use examples for setting sensor alert thresholds. "
                 "Use temperature highs, humidity thresholds, and CO2 danger levels."),
                ("acknowledge_disable.corpus",
                 "Generate 12 tool-use examples for acknowledging and disabling sensor alerts. "
                 "Include false alarm scenarios and maintenance windows."),
            ],
        },
        "historical_data": {
            "tools": "get_historical_readings | get_average_reading | get_min_max | export_sensor_data",
            "call_schema": '{ "func_call": "string", "sensor_id": "string", "from": "string", "to": "string", "interval": "string" }',
            "response_schema": '{ "sensor_id": "string", "readings": [{ "timestamp": "string", "value": number }], "avg": number, "min": number, "max": number }',
            "angles": [
                ("historical_average.corpus",
                 "Generate 12 tool-use examples for fetching historical sensor data and averages. "
                 "Use hourly, daily, and weekly intervals with realistic date ranges."),
                ("minmax_export.corpus",
                 "Generate 12 tool-use examples for getting min/max readings and exporting sensor data. "
                 "Include CSV export and anomaly detection scenarios."),
            ],
        },
    },
    "file_storage": {
        "upload_download": {
            "tools": "upload_file | download_file | get_upload_url | get_download_url",
            "call_schema": '{ "func_call": "string", "path": "string", "file_name": "string", "size_bytes": number, "content_type": "string" }',
            "response_schema": '{ "file_id": "string", "path": "string", "size_bytes": number, "url": "string", "expires_at": "string" }',
            "angles": [
                ("upload.corpus",
                 "Generate 12 tool-use examples for uploading files to cloud storage. "
                 "Use realistic file names, paths (documents/, images/, backups/), and sizes."),
                ("download.corpus",
                 "Generate 12 tool-use examples for downloading files and generating download URLs. "
                 "Include time-limited presigned URLs and direct downloads."),
            ],
        },
        "organize_files": {
            "tools": "create_folder | move_file | copy_file | rename_file | delete_file | list_folder",
            "call_schema": '{ "func_call": "string", "path": "string", "destination": "string", "new_name": "string" }',
            "response_schema": '{ "path": "string", "entries": [{ "name": "string", "type": "file|folder", "size_bytes": number }], "status": "string" }',
            "angles": [
                ("create_move.corpus",
                 "Generate 12 tool-use examples for creating folders and moving files in cloud storage. "
                 "Use realistic directory structures (projects/, archives/, shared/)."),
                ("rename_delete_list.corpus",
                 "Generate 12 tool-use examples for renaming, deleting, and listing files. "
                 "Include cleanup operations and folder navigation."),
            ],
        },
        "sharing_permissions": {
            "tools": "share_file | set_permissions | get_shared_link | revoke_access | list_collaborators",
            "call_schema": '{ "func_call": "string", "file_id": "string", "user_email": "string", "permission": "view|comment|edit", "expires_at": "string" }',
            "response_schema": '{ "file_id": "string", "shared_link": "string", "collaborators": [{ "email": "string", "permission": "string" }] }',
            "angles": [
                ("share_permissions.corpus",
                 "Generate 12 tool-use examples for sharing files and setting permissions. "
                 "Use view/edit/comment access levels and expiry dates."),
                ("revoke_collaborators.corpus",
                 "Generate 12 tool-use examples for revoking file access and listing collaborators. "
                 "Include team sharing and link deactivation scenarios."),
            ],
        },
    },
    "notifications": {
        "push_notifications": {
            "tools": "send_push | send_bulk_push | get_push_status | cancel_push",
            "call_schema": '{ "func_call": "string", "user_id": "string", "title": "string", "body": "string", "data": {}, "device_token": "string" }',
            "response_schema": '{ "notification_id": "string", "status": "sent|delivered|failed", "timestamp": "string" }',
            "angles": [
                ("send_push.corpus",
                 "Generate 12 tool-use examples for sending push notifications to mobile devices. "
                 "Use realistic notification titles, body text, and user IDs."),
                ("bulk_status.corpus",
                 "Generate 12 tool-use examples for bulk push notifications and checking delivery status. "
                 "Include marketing campaigns and system alerts."),
            ],
        },
        "sms_messaging": {
            "tools": "send_sms | send_bulk_sms | get_sms_status | get_sms_history",
            "call_schema": '{ "func_call": "string", "to": "string", "message": "string", "from": "string" }',
            "response_schema": '{ "message_id": "string", "to": "string", "status": "string", "cost": number, "timestamp": "string" }',
            "angles": [
                ("send_sms.corpus",
                 "Generate 12 tool-use examples for sending SMS messages. "
                 "Use E.164 phone number format, OTP codes, delivery confirmations, and alerts."),
                ("bulk_history.corpus",
                 "Generate 12 tool-use examples for bulk SMS campaigns and message history. "
                 "Include marketing, verification, and appointment reminder scenarios."),
            ],
        },
        "scheduled_notifications": {
            "tools": "schedule_notification | cancel_scheduled | list_scheduled | update_schedule",
            "call_schema": '{ "func_call": "string", "notification_id": "string", "scheduled_at": "string", "recurrence": "string", "channel": "push|sms|email" }',
            "response_schema": '{ "notification_id": "string", "scheduled_at": "string", "status": "scheduled|cancelled", "recurrence": "string" }',
            "angles": [
                ("schedule_cancel.corpus",
                 "Generate 12 tool-use examples for scheduling and cancelling future notifications. "
                 "Use ISO 8601 timestamps and daily/weekly recurrence patterns."),
                ("list_update.corpus",
                 "Generate 12 tool-use examples for listing and updating scheduled notifications. "
                 "Include time-zone considerations and multi-channel notifications."),
            ],
        },
    },
    "maps_navigation": {
        "routing": {
            "tools": "get_directions | get_route_alternatives | get_travel_time | get_traffic_conditions",
            "call_schema": '{ "func_call": "string", "origin": "string", "destination": "string", "mode": "driving|walking|cycling|transit" }',
            "response_schema": '{ "distance_km": number, "duration_minutes": number, "steps": [{ "instruction": "string", "distance_km": number }] }',
            "angles": [
                ("driving_transit.corpus",
                 "Generate 12 tool-use examples for getting driving and transit directions. "
                 "Use real city intersections, landmarks, and transit modes. Include realistic distances."),
                ("walking_cycling.corpus",
                 "Generate 12 tool-use examples for walking and cycling routes. "
                 "Use park routes, commute paths, and tourist destinations."),
            ],
        },
        "places_search": {
            "tools": "search_places | get_place_details | find_nearby | get_place_reviews",
            "call_schema": '{ "func_call": "string", "query": "string", "location": "string", "radius_km": number, "type": "string" }',
            "response_schema": '{ "places": [{ "id": "string", "name": "string", "address": "string", "rating": number, "open_now": boolean }], "total": number }',
            "angles": [
                ("search_nearby.corpus",
                 "Generate 12 tool-use examples for searching and finding nearby places. "
                 "Use restaurant, hospital, ATM, gas station, hotel queries near real cities."),
                ("details_reviews.corpus",
                 "Generate 12 tool-use examples for getting place details and reviews. "
                 "Include business hours, ratings, and review summaries."),
            ],
        },
        "geocoding": {
            "tools": "geocode_address | reverse_geocode | validate_address | get_timezone",
            "call_schema": '{ "func_call": "string", "address": "string", "lat": number, "lng": number }',
            "response_schema": '{ "lat": number, "lng": number, "formatted_address": "string", "country": "string", "timezone": "string" }',
            "angles": [
                ("geocode.corpus",
                 "Generate 12 tool-use examples for geocoding addresses to coordinates. "
                 "Use real street addresses from major cities worldwide."),
                ("reverse_timezone.corpus",
                 "Generate 12 tool-use examples for reverse geocoding coordinates and getting timezone. "
                 "Use realistic lat/lng pairs from known locations."),
            ],
        },
    },
    "social_media": {
        "post_creation": {
            "tools": "create_post | create_story | schedule_post | delete_post",
            "call_schema": '{ "func_call": "string", "content": "string", "media_url": "string", "hashtags": ["string"], "scheduled_at": "string" }',
            "response_schema": '{ "post_id": "string", "status": "published|scheduled|draft", "url": "string", "timestamp": "string" }',
            "angles": [
                ("create_schedule.corpus",
                 "Generate 12 tool-use examples for creating and scheduling social media posts. "
                 "Use realistic captions, hashtags, and scheduled timestamps."),
                ("story_delete.corpus",
                 "Generate 12 tool-use examples for creating stories and deleting posts. "
                 "Include business announcements, personal stories, and content moderation."),
            ],
        },
        "social_interactions": {
            "tools": "like_post | comment_on_post | share_post | follow_user | unfollow_user | send_dm",
            "call_schema": '{ "func_call": "string", "post_id": "string", "user_id": "string", "content": "string" }',
            "response_schema": '{ "action": "string", "status": "string", "timestamp": "string" }',
            "angles": [
                ("like_comment.corpus",
                 "Generate 12 tool-use examples for liking and commenting on posts. "
                 "Use realistic comment text and post IDs."),
                ("follow_dm.corpus",
                 "Generate 12 tool-use examples for following users and sending direct messages. "
                 "Use realistic usernames and DM conversation scenarios."),
            ],
        },
        "search_discover": {
            "tools": "search_posts | search_users | get_trending_hashtags | get_explore_feed",
            "call_schema": '{ "func_call": "string", "query": "string", "hashtag": "string", "location": "string", "limit": number }',
            "response_schema": '{ "results": [{ "id": "string", "type": "post|user", "content": "string", "likes": number }], "total": number }',
            "angles": [
                ("search_posts_users.corpus",
                 "Generate 12 tool-use examples for searching posts and users on social media. "
                 "Use realistic queries, hashtags, and result objects."),
                ("trending_explore.corpus",
                 "Generate 12 tool-use examples for getting trending hashtags and explore feed. "
                 "Include location-based trending and category filtering."),
            ],
        },
    },
    "hr_system": {
        "employee_lookup": {
            "tools": "search_employee | get_employee_by_id | get_org_chart | list_employees_by_department",
            "call_schema": '{ "func_call": "string", "query": "string", "department": "string", "employee_id": "string" }',
            "response_schema": '{ "employees": [{ "id": "string", "name": "string", "title": "string", "department": "string", "email": "string", "manager": "string" }] }',
            "angles": [
                ("search_by_name.corpus",
                 "Generate 12 tool-use examples for looking up employees by name and ID. "
                 "Use realistic full names, job titles, and departments."),
                ("org_chart_dept.corpus",
                 "Generate 12 tool-use examples for fetching org charts and department rosters. "
                 "Use Engineering, Sales, HR, Finance, Marketing departments."),
            ],
        },
        "leave_management": {
            "tools": "request_leave | get_leave_balance | approve_leave | reject_leave | get_leave_history",
            "call_schema": '{ "func_call": "string", "employee_id": "string", "leave_type": "vacation|sick|personal|parental", "from_date": "string", "to_date": "string" }',
            "response_schema": '{ "request_id": "string", "status": "pending|approved|rejected", "days_requested": number, "balance_remaining": number }',
            "angles": [
                ("request_balance.corpus",
                 "Generate 12 tool-use examples for requesting leave and checking leave balance. "
                 "Use vacation, sick, and personal leave types with realistic date ranges."),
                ("approve_reject.corpus",
                 "Generate 12 tool-use examples for approving and rejecting leave requests. "
                 "Include manager approval flows and rejection reasons."),
            ],
        },
        "payroll": {
            "tools": "get_payslip | get_salary_info | run_payroll | update_tax_info | get_ytd_earnings",
            "call_schema": '{ "func_call": "string", "employee_id": "string", "period": "string" }',
            "response_schema": '{ "employee_id": "string", "period": "string", "gross": number, "deductions": number, "net": number, "currency": "string" }',
            "angles": [
                ("payslip_salary.corpus",
                 "Generate 12 tool-use examples for getting payslips and salary information. "
                 "Use monthly/biweekly periods and realistic salary ranges."),
                ("ytd_tax.corpus",
                 "Generate 12 tool-use examples for year-to-date earnings and tax information updates. "
                 "Include W-4 updates and annual tax summary scenarios."),
            ],
        },
    },
    "healthcare": {
        "appointments": {
            "tools": "book_appointment | cancel_appointment | reschedule_appointment | get_upcoming_appointments | get_available_slots",
            "call_schema": '{ "func_call": "string", "patient_id": "string", "doctor_id": "string", "specialty": "string", "date": "string", "reason": "string" }',
            "response_schema": '{ "appointment_id": "string", "doctor": "string", "date": "string", "time": "string", "location": "string", "status": "string" }',
            "angles": [
                ("book_cancel.corpus",
                 "Generate 12 tool-use examples for booking and cancelling medical appointments. "
                 "Use specialties (GP, cardiology, dermatology, pediatrics) and realistic doctor names."),
                ("reschedule_slots.corpus",
                 "Generate 12 tool-use examples for rescheduling appointments and finding available slots. "
                 "Include urgent and routine appointment scenarios."),
            ],
        },
        "prescriptions": {
            "tools": "get_prescriptions | request_refill | check_drug_interaction | get_medication_info",
            "call_schema": '{ "func_call": "string", "patient_id": "string", "medication": "string", "dosage": "string" }',
            "response_schema": '{ "prescription_id": "string", "medication": "string", "dosage": "string", "refills_remaining": number, "status": "string" }',
            "angles": [
                ("get_refill.corpus",
                 "Generate 12 tool-use examples for getting prescriptions and requesting refills. "
                 "Use common medications (metformin, lisinopril, atorvastatin) and realistic dosages."),
                ("interaction_info.corpus",
                 "Generate 12 tool-use examples for checking drug interactions and getting medication info. "
                 "Include common drug pair checks and contraindication responses."),
            ],
        },
        "lab_results": {
            "tools": "get_lab_results | get_latest_results | get_result_history | download_report",
            "call_schema": '{ "func_call": "string", "patient_id": "string", "test_type": "string", "from_date": "string" }',
            "response_schema": '{ "results": [{ "test": "string", "value": number, "unit": "string", "reference_range": "string", "status": "normal|high|low" }] }',
            "angles": [
                ("blood_panel.corpus",
                 "Generate 12 tool-use examples for getting blood panel lab results. "
                 "Use realistic CBC, cholesterol, glucose, and HbA1c values with reference ranges."),
                ("history_download.corpus",
                 "Generate 12 tool-use examples for lab result history and report downloads. "
                 "Include trending results over time and PDF report generation."),
            ],
        },
    },
    "travel_booking": {
        "flight_search": {
            "tools": "search_flights | get_flight_details | filter_flights | get_seat_map",
            "call_schema": '{ "func_call": "string", "origin": "string", "destination": "string", "departure_date": "string", "return_date": "string", "passengers": number, "cabin": "economy|business|first" }',
            "response_schema": '{ "flights": [{ "flight_number": "string", "airline": "string", "departure": "string", "arrival": "string", "price": number, "duration_minutes": number }], "total": number }',
            "angles": [
                ("one_way_roundtrip.corpus",
                 "Generate 12 tool-use examples for searching one-way and round-trip flights. "
                 "Use real airport codes (JFK, LHR, CDG, NRT) and realistic prices."),
                ("cabin_filters.corpus",
                 "Generate 12 tool-use examples for filtering flights by cabin class and preferences. "
                 "Include business, economy, direct flight, and stopover filters."),
            ],
        },
        "hotel_booking": {
            "tools": "search_hotels | get_hotel_details | book_hotel | cancel_hotel | get_amenities",
            "call_schema": '{ "func_call": "string", "location": "string", "check_in": "string", "check_out": "string", "guests": number, "min_rating": number }',
            "response_schema": '{ "hotels": [{ "id": "string", "name": "string", "rating": number, "price_per_night": number, "amenities": ["string"] }], "total": number }',
            "angles": [
                ("search_book.corpus",
                 "Generate 12 tool-use examples for searching and booking hotels. "
                 "Use real city names, check-in/out dates, and realistic price ranges."),
                ("details_cancel.corpus",
                 "Generate 12 tool-use examples for getting hotel details and cancelling reservations. "
                 "Include amenity lists and free cancellation policies."),
            ],
        },
        "car_rental": {
            "tools": "search_cars | book_car | cancel_rental | get_rental_details | extend_rental",
            "call_schema": '{ "func_call": "string", "location": "string", "pickup_date": "string", "return_date": "string", "car_type": "economy|compact|suv|luxury" }',
            "response_schema": '{ "rental_id": "string", "car": "string", "pickup_location": "string", "daily_rate": number, "total_cost": number }',
            "angles": [
                ("search_book_car.corpus",
                 "Generate 12 tool-use examples for searching and booking rental cars. "
                 "Use airport pickups, weekly rentals, and varied car categories."),
                ("extend_cancel.corpus",
                 "Generate 12 tool-use examples for extending and cancelling car rentals. "
                 "Include late return fees and cancellation policies."),
            ],
        },
    },
    "customer_support": {
        "create_ticket": {
            "tools": "create_ticket | create_urgent_ticket | attach_file | link_order",
            "call_schema": '{ "func_call": "string", "customer_id": "string", "subject": "string", "description": "string", "priority": "low|medium|high|urgent", "category": "string" }',
            "response_schema": '{ "ticket_id": "string", "status": "open", "priority": "string", "assigned_to": "string", "created_at": "string" }',
            "angles": [
                ("create_standard.corpus",
                 "Generate 12 tool-use examples for creating support tickets. "
                 "Use realistic issue descriptions (billing, shipping, login, product defect) and priority levels."),
                ("urgent_attach.corpus",
                 "Generate 12 tool-use examples for urgent tickets and attaching files. "
                 "Include outage reports, security issues, and screenshot attachments."),
            ],
        },
        "ticket_status": {
            "tools": "get_ticket_status | list_open_tickets | add_reply | close_ticket | reopen_ticket",
            "call_schema": '{ "func_call": "string", "ticket_id": "string", "customer_id": "string", "reply": "string" }',
            "response_schema": '{ "ticket_id": "string", "status": "open|in_progress|resolved|closed", "replies": [{ "author": "string", "message": "string", "timestamp": "string" }] }',
            "angles": [
                ("status_reply.corpus",
                 "Generate 12 tool-use examples for checking ticket status and adding replies. "
                 "Use realistic support conversation exchanges."),
                ("close_reopen.corpus",
                 "Generate 12 tool-use examples for closing and reopening support tickets. "
                 "Include resolution confirmations and follow-up scenarios."),
            ],
        },
        "escalation": {
            "tools": "escalate_ticket | transfer_to_specialist | get_escalation_status | set_sla",
            "call_schema": '{ "func_call": "string", "ticket_id": "string", "reason": "string", "target_team": "string" }',
            "response_schema": '{ "ticket_id": "string", "escalated_to": "string", "reason": "string", "sla_hours": number, "status": "string" }',
            "angles": [
                ("escalate_transfer.corpus",
                 "Generate 12 tool-use examples for escalating tickets and transferring to specialists. "
                 "Use tier 2 support, billing team, and technical escalation scenarios."),
                ("sla_status.corpus",
                 "Generate 12 tool-use examples for setting SLA targets and checking escalation status. "
                 "Include breach warnings and resolution deadline tracking."),
            ],
        },
    },
    "git_api": {
        "repository_ops": {
            "tools": "create_repo | delete_repo | fork_repo | get_repo_info | list_repos",
            "call_schema": '{ "func_call": "string", "owner": "string", "repo": "string", "description": "string", "private": boolean }',
            "response_schema": '{ "repo": "string", "owner": "string", "url": "string", "stars": number, "forks": number, "default_branch": "string" }',
            "angles": [
                ("create_fork.corpus",
                 "Generate 12 tool-use examples for creating and forking repositories. "
                 "Use realistic repo names, descriptions, and owner usernames."),
                ("info_list.corpus",
                 "Generate 12 tool-use examples for getting repo info and listing repositories. "
                 "Include public/private repos with realistic star counts."),
            ],
        },
        "commits_branches": {
            "tools": "list_commits | get_commit | create_branch | delete_branch | list_branches | compare_branches",
            "call_schema": '{ "func_call": "string", "owner": "string", "repo": "string", "branch": "string", "sha": "string" }',
            "response_schema": '{ "commits": [{ "sha": "string", "message": "string", "author": "string", "date": "string" }], "branch": "string" }',
            "angles": [
                ("commits.corpus",
                 "Generate 12 tool-use examples for listing and getting commit details. "
                 "Use realistic commit SHAs, messages (feat:, fix:, chore:), and author names."),
                ("branches.corpus",
                 "Generate 12 tool-use examples for creating, deleting, and listing branches. "
                 "Use branch naming conventions (feature/, bugfix/, release/)."),
            ],
        },
        "pull_requests": {
            "tools": "create_pr | list_prs | merge_pr | close_pr | add_pr_review | get_pr_diff",
            "call_schema": '{ "func_call": "string", "owner": "string", "repo": "string", "pr_number": number, "title": "string", "head": "string", "base": "string" }',
            "response_schema": '{ "pr_number": number, "title": "string", "state": "open|merged|closed", "author": "string", "changed_files": number, "mergeable": boolean }',
            "angles": [
                ("create_list_pr.corpus",
                 "Generate 12 tool-use examples for creating and listing pull requests. "
                 "Use realistic PR titles, feature branch names, and descriptions."),
                ("merge_review.corpus",
                 "Generate 12 tool-use examples for merging PRs and adding reviews. "
                 "Include approval, request changes, and merge conflict scenarios."),
            ],
        },
    },
    "docker_api": {
        "container_lifecycle": {
            "tools": "run_container | stop_container | start_container | remove_container | list_containers",
            "call_schema": '{ "func_call": "string", "container_id": "string", "image": "string", "name": "string", "ports": "string", "env": ["string"] }',
            "response_schema": '{ "container_id": "string", "name": "string", "image": "string", "state": "running|stopped|exited", "ports": "string" }',
            "angles": [
                ("run_stop.corpus",
                 "Generate 12 tool-use examples for running and stopping Docker containers. "
                 "Use real Docker images (nginx, postgres, redis, node, python) with port mappings."),
                ("remove_list.corpus",
                 "Generate 12 tool-use examples for removing and listing containers. "
                 "Include filter by state and force remove scenarios."),
            ],
        },
        "image_management": {
            "tools": "pull_image | push_image | build_image | list_images | remove_image | tag_image",
            "call_schema": '{ "func_call": "string", "image": "string", "tag": "string", "registry": "string", "dockerfile": "string" }',
            "response_schema": '{ "image_id": "string", "repository": "string", "tag": "string", "size_mb": number, "created": "string" }',
            "angles": [
                ("pull_push.corpus",
                 "Generate 12 tool-use examples for pulling and pushing Docker images. "
                 "Use Docker Hub and private registry scenarios with realistic image names and tags."),
                ("build_tag.corpus",
                 "Generate 12 tool-use examples for building and tagging images. "
                 "Use semantic versioning tags (v1.0.0, latest, staging) and Dockerfile paths."),
            ],
        },
        "network_volumes": {
            "tools": "create_network | list_networks | create_volume | list_volumes | mount_volume",
            "call_schema": '{ "func_call": "string", "name": "string", "driver": "string", "container_id": "string", "mount_path": "string" }',
            "response_schema": '{ "id": "string", "name": "string", "driver": "string", "scope": "string", "containers": ["string"] }',
            "angles": [
                ("network_ops.corpus",
                 "Generate 12 tool-use examples for creating and listing Docker networks. "
                 "Use bridge, host, overlay drivers and realistic network names."),
                ("volume_ops.corpus",
                 "Generate 12 tool-use examples for creating volumes and mounting them to containers. "
                 "Use data persistence scenarios for databases and application logs."),
            ],
        },
    },
    "payment_processing": {
        "charge_refund": {
            "tools": "charge_card | partial_refund | full_refund | capture_payment | void_payment",
            "call_schema": '{ "func_call": "string", "customer_id": "string", "amount": number, "currency": "string", "payment_method_id": "string", "description": "string" }',
            "response_schema": '{ "transaction_id": "string", "status": "succeeded|failed|pending", "amount": number, "currency": "string" }',
            "angles": [
                ("charge_capture.corpus",
                 "Generate 12 tool-use examples for charging cards and capturing payments. "
                 "Use USD, EUR, GBP amounts with realistic descriptions and customer IDs."),
                ("refund_void.corpus",
                 "Generate 12 tool-use examples for issuing refunds and voiding payments. "
                 "Include partial refund and full refund scenarios with reasons."),
            ],
        },
        "subscription": {
            "tools": "create_subscription | cancel_subscription | pause_subscription | update_plan | get_subscription",
            "call_schema": '{ "func_call": "string", "customer_id": "string", "plan_id": "string", "trial_days": number }',
            "response_schema": '{ "subscription_id": "string", "status": "active|canceled|paused|trialing", "plan": "string", "current_period_end": "string" }',
            "angles": [
                ("create_cancel.corpus",
                 "Generate 12 tool-use examples for creating and cancelling subscriptions. "
                 "Use SaaS plan names (starter, pro, enterprise) and trial periods."),
                ("pause_upgrade.corpus",
                 "Generate 12 tool-use examples for pausing and upgrading subscription plans. "
                 "Include proration and immediate vs. end-of-period changes."),
            ],
        },
        "transaction_lookup": {
            "tools": "get_transaction | list_transactions | search_transactions | get_balance",
            "call_schema": '{ "func_call": "string", "transaction_id": "string", "customer_id": "string", "from_date": "string", "to_date": "string" }',
            "response_schema": '{ "transactions": [{ "id": "string", "amount": number, "currency": "string", "status": "string", "created": "string" }], "total_count": number }',
            "angles": [
                ("lookup_list.corpus",
                 "Generate 12 tool-use examples for looking up and listing payment transactions. "
                 "Use realistic transaction IDs and customer IDs."),
                ("search_balance.corpus",
                 "Generate 12 tool-use examples for searching transactions and getting account balance. "
                 "Include date range filtering and currency-specific balance queries."),
            ],
        },
    },
    "inventory_management": {
        "stock_levels": {
            "tools": "get_stock_level | check_availability | get_low_stock_items | get_stock_by_location",
            "call_schema": '{ "func_call": "string", "sku": "string", "location_id": "string", "threshold": number }',
            "response_schema": '{ "sku": "string", "product_name": "string", "quantity": number, "location": "string", "status": "in_stock|low_stock|out_of_stock" }',
            "angles": [
                ("check_levels.corpus",
                 "Generate 12 tool-use examples for checking stock levels and availability. "
                 "Use realistic SKUs, product names, and warehouse locations."),
                ("low_stock_location.corpus",
                 "Generate 12 tool-use examples for finding low-stock items and stock by location. "
                 "Include reorder threshold alerts and multi-warehouse scenarios."),
            ],
        },
        "reorder": {
            "tools": "create_purchase_order | get_po_status | cancel_po | get_reorder_suggestions",
            "call_schema": '{ "func_call": "string", "sku": "string", "quantity": number, "supplier_id": "string", "expected_delivery": "string" }',
            "response_schema": '{ "po_id": "string", "sku": "string", "quantity": number, "supplier": "string", "status": "string", "expected_delivery": "string" }',
            "angles": [
                ("create_po.corpus",
                 "Generate 12 tool-use examples for creating purchase orders. "
                 "Use realistic supplier names, quantities, and delivery lead times."),
                ("reorder_suggestions.corpus",
                 "Generate 12 tool-use examples for getting reorder suggestions and PO status. "
                 "Include auto-reorder triggers and safety stock calculations."),
            ],
        },
        "warehouse_ops": {
            "tools": "transfer_stock | receive_shipment | adjust_inventory | get_receiving_log",
            "call_schema": '{ "func_call": "string", "sku": "string", "from_location": "string", "to_location": "string", "quantity": number, "reason": "string" }',
            "response_schema": '{ "transaction_id": "string", "sku": "string", "quantity": number, "from": "string", "to": "string", "status": "string" }',
            "angles": [
                ("transfer_receive.corpus",
                 "Generate 12 tool-use examples for transferring stock between warehouses and receiving shipments. "
                 "Use location codes (WH-A, WH-B, STORE-01) and realistic quantities."),
                ("adjust_log.corpus",
                 "Generate 12 tool-use examples for inventory adjustments and receiving logs. "
                 "Include damage writeoff, cycle count adjustments, and receiving discrepancies."),
            ],
        },
    },
    "analytics": {
        "page_views": {
            "tools": "get_page_views | get_unique_visitors | get_session_duration | get_bounce_rate",
            "call_schema": '{ "func_call": "string", "url": "string", "from_date": "string", "to_date": "string", "granularity": "hourly|daily|weekly|monthly" }',
            "response_schema": '{ "url": "string", "period": "string", "views": number, "unique_visitors": number, "avg_session_seconds": number, "bounce_rate": number }',
            "angles": [
                ("page_views_visitors.corpus",
                 "Generate 12 tool-use examples for getting page view counts and unique visitor data. "
                 "Use realistic website URLs and date ranges with plausible traffic numbers."),
                ("session_bounce.corpus",
                 "Generate 12 tool-use examples for session duration and bounce rate analytics. "
                 "Use realistic metrics for e-commerce, blog, and SaaS product pages."),
            ],
        },
        "conversion_events": {
            "tools": "get_conversion_rate | track_event | get_funnel_data | get_goal_completions",
            "call_schema": '{ "func_call": "string", "event_name": "string", "funnel_id": "string", "from_date": "string", "to_date": "string" }',
            "response_schema": '{ "event": "string", "total_events": number, "unique_users": number, "conversion_rate": number, "funnel_steps": [{ "name": "string", "completions": number }] }',
            "angles": [
                ("conversion_funnel.corpus",
                 "Generate 12 tool-use examples for getting conversion rates and funnel data. "
                 "Use checkout, signup, and onboarding funnels with realistic drop-off rates."),
                ("events_goals.corpus",
                 "Generate 12 tool-use examples for tracking custom events and goal completions. "
                 "Use button clicks, form submissions, and purchase events."),
            ],
        },
        "custom_reports": {
            "tools": "create_report | get_report | list_reports | schedule_report | export_report",
            "call_schema": '{ "func_call": "string", "report_id": "string", "name": "string", "metrics": ["string"], "dimensions": ["string"], "from_date": "string", "to_date": "string" }',
            "response_schema": '{ "report_id": "string", "name": "string", "rows": [{}], "total_rows": number, "generated_at": "string" }',
            "angles": [
                ("create_get_report.corpus",
                 "Generate 12 tool-use examples for creating and fetching custom analytics reports. "
                 "Use metrics (sessions, revenue, ctr) and dimensions (country, device, source)."),
                ("schedule_export.corpus",
                 "Generate 12 tool-use examples for scheduling recurring reports and exporting data. "
                 "Include daily email reports, CSV exports, and dashboard snapshots."),
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# tool_use_2 — complex schemas, nested responses, batch ops, error handling
# Same builder as tool_use; lives in corpus/tool_use_2/
# All angles request 20 examples (vs 12 in tool_use) for more data per file.
# ---------------------------------------------------------------------------

BASE_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus", "tool_use_2")

TOOL_DOMAINS_2 = {
    "complex_api": {
        "nested_responses": {
            "tools": "get_user_profile | get_order_with_items | get_dashboard_summary",
            "call_schema": '{ "func_call": "string", "id": "string", "include": ["string"] }',
            "response_schema": '{ "id": "string", "data": { "profile": {}, "stats": {}, "recent": [{}] } }',
            "angles": [
                ("user_profile_nested.corpus",
                 "Generate 20 tool-use examples for fetching deeply nested user profile data. "
                 "Responses must include nested objects: address {street, city, country}, preferences {theme, language}, stats {logins, purchases}. "
                 "Use realistic names, emails, and nested field values."),
                ("order_with_items.corpus",
                 "Generate 20 tool-use examples for fetching an order with nested line items. "
                 "Responses include: order metadata, items array (each with product_id, name, qty, unit_price), and a totals object {subtotal, tax, shipping, total}. "
                 "Use realistic product names and prices."),
            ],
        },
        "batch_operations": {
            "tools": "batch_create | batch_update | batch_delete | batch_get",
            "call_schema": '{ "func_call": "string", "items": [{}], "options": { "on_error": "stop|skip", "dry_run": boolean } }',
            "response_schema": '{ "processed": number, "succeeded": number, "failed": number, "errors": [{ "index": number, "id": "string", "reason": "string" }], "results": [{}] }',
            "angles": [
                ("batch_create_users.corpus",
                 "Generate 20 tool-use examples for batch-creating users or records. "
                 "Input items arrays should have 3–5 elements each with realistic fields. "
                 "Some responses should include partial failures with error reasons."),
                ("batch_update_status.corpus",
                 "Generate 20 tool-use examples for batch-updating status fields across orders, tickets, or accounts. "
                 "Include dry_run=true examples and on_error=skip scenarios with realistic partial failure responses."),
            ],
        },
        "paginated_results": {
            "tools": "list_users | list_orders | list_events | list_products",
            "call_schema": '{ "func_call": "string", "page": number, "page_size": number, "sort_by": "string", "sort_dir": "asc|desc", "filters": {} }',
            "response_schema": '{ "items": [{}], "pagination": { "page": number, "page_size": number, "total_items": number, "total_pages": number, "has_next": boolean, "next_cursor": "string" } }',
            "angles": [
                ("paginate_users.corpus",
                 "Generate 20 tool-use examples for paginating through user or customer lists. "
                 "Vary page sizes (10, 25, 50, 100), sort fields, and filter combinations. "
                 "Responses should include realistic pagination metadata and 3–5 item objects each."),
                ("paginate_events_cursor.corpus",
                 "Generate 20 tool-use examples for cursor-based pagination through event logs or order history. "
                 "Include first page, middle page, and last page scenarios. "
                 "Responses should have realistic next_cursor tokens and has_next values."),
            ],
        },
        "error_responses": {
            "tools": "get_resource | create_resource | update_resource | delete_resource",
            "call_schema": '{ "func_call": "string", "id": "string", "data": {} }',
            "response_schema": '{ "success": boolean, "error": { "code": "string", "message": "string", "field": "string", "details": {} } }',
            "angles": [
                ("not_found_unauthorized.corpus",
                 "Generate 20 tool-use examples where the API call fails. "
                 "Mix NOT_FOUND (resource doesn't exist), UNAUTHORIZED (missing/expired token), and FORBIDDEN (insufficient permissions) errors. "
                 "Use realistic error messages and resource IDs."),
                ("validation_rate_limit.corpus",
                 "Generate 20 tool-use examples for validation errors and rate limit responses. "
                 "Validation errors should include the failing field name and reason (required, too_short, invalid_format). "
                 "Rate limit responses should include retry_after seconds."),
            ],
        },
        "webhook_events": {
            "tools": "handle_payment_event | handle_user_event | handle_order_event | handle_system_event",
            "call_schema": '{ "func_call": "string", "event_type": "string", "event_id": "string", "timestamp": "string", "payload": {} }',
            "response_schema": '{ "event_id": "string", "event_type": "string", "status": "processed|ignored|failed", "payload": { "object": "string", "data": {} } }',
            "angles": [
                ("payment_webhook.corpus",
                 "Generate 20 tool-use examples for incoming payment webhook events (charge.succeeded, charge.failed, refund.created, subscription.renewed). "
                 "Payloads should include nested customer, amount, and metadata objects with realistic values."),
                ("user_order_webhook.corpus",
                 "Generate 20 tool-use examples for user lifecycle and order status webhook events (user.created, user.deleted, order.shipped, order.delivered). "
                 "Include realistic nested payload objects with timestamps, IDs, and status transitions."),
            ],
        },
    },
    "weather_api": {
        "multi_location_forecast": {
            "tools": "get_multi_location_forecast | compare_weather | get_regional_summary",
            "call_schema": '{ "func_call": "string", "locations": ["string"], "days": number, "metrics": ["string"] }',
            "response_schema": '{ "locations": [{ "name": "string", "country": "string", "forecast": [{ "date": "string", "high": number, "low": number, "precip_mm": number, "wind_kph": number, "condition": "string" }] }] }',
            "angles": [
                ("multi_city_forecast.corpus",
                 "Generate 20 tool-use examples for fetching 5-day forecasts for 3–5 cities simultaneously. "
                 "Responses include per-city forecast arrays with temperature, precipitation, and wind. "
                 "Use real city groupings (European capitals, US coastal cities, Asian megacities)."),
                ("compare_weather.corpus",
                 "Generate 20 tool-use examples for comparing weather across multiple locations. "
                 "Questions like 'Which city will be warmest this weekend?' or 'Compare rain in London and Amsterdam'. "
                 "Responses include structured comparison data for each location."),
            ],
        },
    },
    "ecommerce": {
        "cart_with_promotions": {
            "tools": "get_cart_summary | apply_promotion | calculate_shipping | estimate_tax",
            "call_schema": '{ "func_call": "string", "cart_id": "string", "promo_code": "string", "shipping_address": { "country": "string", "state": "string", "zip": "string" } }',
            "response_schema": '{ "cart_id": "string", "items": [{ "sku": "string", "name": "string", "qty": number, "unit_price": number, "line_total": number }], "promotions": [{ "code": "string", "type": "string", "discount": number }], "totals": { "subtotal": number, "discount": number, "shipping": number, "tax": number, "grand_total": number } }',
            "angles": [
                ("cart_with_discount.corpus",
                 "Generate 20 tool-use examples for cart summaries with applied discount codes. "
                 "Carts should have 3–6 line items. Promotions include percent-off, flat discount, and free-shipping codes. "
                 "Totals object must be arithmetically consistent."),
                ("cart_shipping_tax.corpus",
                 "Generate 20 tool-use examples for calculating shipping and tax on a cart. "
                 "Use varied shipping addresses (US states, EU countries, Canada). "
                 "Include flat-rate, weight-based, and free-over-threshold shipping scenarios."),
            ],
        },
        "product_variants": {
            "tools": "get_product_with_variants | get_variant_inventory | configure_product",
            "call_schema": '{ "func_call": "string", "product_id": "string", "options": { "color": "string", "size": "string", "material": "string" } }',
            "response_schema": '{ "product_id": "string", "name": "string", "variants": [{ "sku": "string", "options": {}, "price": number, "stock": number, "images": ["string"] }], "selected_variant": {} }',
            "angles": [
                ("clothing_variants.corpus",
                 "Generate 20 tool-use examples for fetching clothing product variants (size × color combinations). "
                 "Each response includes 4–8 variants with SKUs, prices, and stock levels. "
                 "Use realistic clothing product names and option combinations."),
                ("electronics_variants.corpus",
                 "Generate 20 tool-use examples for electronics products with storage/color/model variants. "
                 "Examples: phones (128GB/256GB × color), laptops (RAM/SSD combos). "
                 "Responses include nested options and per-variant pricing."),
            ],
        },
    },
    "database": {
        "complex_queries": {
            "tools": "query_with_joins | subquery | window_function | upsert_record",
            "call_schema": '{ "func_call": "string", "primary_table": "string", "joins": [{ "table": "string", "on": "string", "type": "inner|left|right" }], "select": ["string"], "where": "string", "order_by": "string", "limit": number }',
            "response_schema": '{ "rows": [{}], "count": number, "query_ms": number, "explain": "string" }',
            "angles": [
                ("join_queries.corpus",
                 "Generate 20 tool-use examples for multi-table JOIN queries. "
                 "Use schemas like users+orders+products, employees+departments+salaries. "
                 "Each response returns 3–6 row objects with fields from multiple tables."),
                ("aggregate_window.corpus",
                 "Generate 20 tool-use examples for aggregate and window function queries. "
                 "Include GROUP BY with HAVING, running totals, rank/dense_rank, and rolling averages. "
                 "Return realistic grouped result rows with computed columns."),
            ],
        },
        "transactions": {
            "tools": "begin_transaction | commit_transaction | rollback_transaction | savepoint",
            "call_schema": '{ "func_call": "string", "transaction_id": "string", "operations": [{ "type": "insert|update|delete", "table": "string", "data": {} }] }',
            "response_schema": '{ "transaction_id": "string", "status": "committed|rolled_back|pending", "operations_applied": number, "duration_ms": number, "error": {} }',
            "angles": [
                ("commit_rollback.corpus",
                 "Generate 20 tool-use examples for database transactions with commit and rollback. "
                 "Each transaction has 2–4 operations across related tables. "
                 "Include successful commits and rollbacks due to constraint violations."),
                ("partial_failure.corpus",
                 "Generate 20 tool-use examples where a transaction partially fails and rolls back. "
                 "Error objects should include the failing operation index, constraint name, and message. "
                 "Use FK violations, unique constraint failures, and null violations."),
            ],
        },
    },
    "cloud_server_api": {
        "infrastructure_as_code": {
            "tools": "deploy_stack | update_stack | destroy_stack | get_stack_status | list_stack_resources",
            "call_schema": '{ "func_call": "string", "stack_name": "string", "template": "string", "parameters": [{ "key": "string", "value": "string" }], "region": "string" }',
            "response_schema": '{ "stack_id": "string", "stack_name": "string", "status": "string", "resources": [{ "type": "string", "name": "string", "state": "string", "id": "string" }], "outputs": [{ "key": "string", "value": "string" }] }',
            "angles": [
                ("deploy_stack.corpus",
                 "Generate 20 tool-use examples for deploying infrastructure stacks. "
                 "Stacks should contain 4–7 resources (EC2, RDS, S3, LoadBalancer, SecurityGroup, etc). "
                 "Use realistic stack names, parameter sets, and output values (endpoint URLs, resource IDs)."),
                ("update_destroy.corpus",
                 "Generate 20 tool-use examples for updating and destroying stacks. "
                 "Updates should show changed parameters and updated resource states. "
                 "Include both clean destroys and destroy-with-retained-resources scenarios."),
            ],
        },
    },
    "crm": {
        "activity_timeline": {
            "tools": "get_contact_timeline | log_activity | get_engagement_score | get_touchpoint_summary",
            "call_schema": '{ "func_call": "string", "contact_id": "string", "activity_type": "call|email|meeting|note|task", "subject": "string", "body": "string", "outcome": "string", "duration_minutes": number }',
            "response_schema": '{ "contact_id": "string", "timeline": [{ "id": "string", "type": "string", "date": "string", "subject": "string", "outcome": "string", "rep": "string" }], "engagement_score": number, "last_touch": "string" }',
            "angles": [
                ("log_call_meeting.corpus",
                 "Generate 20 tool-use examples for logging sales calls and meetings against a contact. "
                 "Include outcomes (connected, voicemail, no-show, demo-completed) and realistic subject lines. "
                 "Responses show the updated timeline with the new activity prepended."),
                ("engagement_timeline.corpus",
                 "Generate 20 tool-use examples for fetching contact engagement timelines. "
                 "Timelines have 5–8 entries mixing calls, emails, and meetings. "
                 "Include engagement score (0–100) and last-touch date."),
            ],
        },
    },
    "banking": {
        "multi_account_summary": {
            "tools": "get_portfolio_summary | get_account_group | get_net_worth | get_cashflow_analysis",
            "call_schema": '{ "func_call": "string", "customer_id": "string", "include_accounts": ["string"], "currency": "string", "as_of_date": "string" }',
            "response_schema": '{ "customer_id": "string", "accounts": [{ "id": "string", "type": "string", "balance": number, "currency": "string" }], "totals": { "assets": number, "liabilities": number, "net_worth": number }, "currency": "string" }',
            "angles": [
                ("portfolio_summary.corpus",
                 "Generate 20 tool-use examples for fetching a customer's full portfolio across all account types. "
                 "Include checking, savings, investment, mortgage, and credit card accounts. "
                 "Totals must be arithmetically consistent. Use USD, EUR, and GBP."),
                ("cashflow_analysis.corpus",
                 "Generate 20 tool-use examples for monthly cashflow analysis. "
                 "Responses include income breakdown, expense categories, and net cashflow. "
                 "Use realistic transaction categories and amounts."),
            ],
        },
    },
    "hr_system": {
        "performance_reviews": {
            "tools": "submit_review | get_review | list_reviews | get_review_summary | set_goals",
            "call_schema": '{ "func_call": "string", "employee_id": "string", "reviewer_id": "string", "period": "string", "ratings": { "performance": number, "communication": number, "teamwork": number, "leadership": number }, "comments": "string", "goals": ["string"] }',
            "response_schema": '{ "review_id": "string", "employee": "string", "period": "string", "overall_score": number, "ratings": {}, "goals": [{ "goal": "string", "status": "not_started|in_progress|completed" }], "submitted_at": "string" }',
            "angles": [
                ("submit_review.corpus",
                 "Generate 20 tool-use examples for submitting employee performance reviews. "
                 "Include ratings (1–5) across 4 dimensions, written comments, and 2–4 goals. "
                 "Use realistic employee names, roles, and review periods (Q1 2024, H2 2023)."),
                ("review_summary.corpus",
                 "Generate 20 tool-use examples for fetching review summaries and goal progress. "
                 "Include averaged scores, goal completion status, and manager comments. "
                 "Use varied performance profiles (high performer, needs improvement, on-track)."),
            ],
        },
    },
    "analytics": {
        "cohort_analysis": {
            "tools": "get_cohort_retention | get_cohort_revenue | get_churn_analysis",
            "call_schema": '{ "func_call": "string", "cohort_period": "weekly|monthly", "start_date": "string", "end_date": "string", "segment": "string", "metric": "string" }',
            "response_schema": '{ "cohort": "string", "cohort_size": number, "periods": [{ "period": number, "retained": number, "retention_rate": number, "revenue": number }] }',
            "angles": [
                ("retention_cohorts.corpus",
                 "Generate 20 tool-use examples for cohort retention analysis. "
                 "Responses should include 6–12 time periods with realistic retention curves (high early drop-off then plateau). "
                 "Use monthly cohorts and segment by acquisition channel."),
                ("revenue_churn.corpus",
                 "Generate 20 tool-use examples for cohort revenue and churn analysis. "
                 "Include MRR expansion, contraction, and churn per cohort period. "
                 "Use SaaS-style metrics with realistic ARR ranges."),
            ],
        },
        "ab_testing": {
            "tools": "create_experiment | get_experiment_results | stop_experiment | get_significance",
            "call_schema": '{ "func_call": "string", "experiment_id": "string", "name": "string", "variants": [{ "id": "string", "name": "string", "traffic_pct": number }], "metric": "string", "min_detectable_effect": number }',
            "response_schema": '{ "experiment_id": "string", "status": "running|stopped|completed", "variants": [{ "id": "string", "name": "string", "visitors": number, "conversions": number, "conversion_rate": number, "lift_pct": number }], "winner": "string", "p_value": number, "significant": boolean }',
            "angles": [
                ("create_run_experiment.corpus",
                 "Generate 20 tool-use examples for creating and checking A/B tests. "
                 "Use 2–3 variants (control + 1–2 treatments) with realistic traffic splits. "
                 "Test names should reflect real product experiments (button color, CTA text, checkout flow)."),
                ("results_significance.corpus",
                 "Generate 20 tool-use examples for fetching A/B test results and statistical significance. "
                 "Include both significant winners (p < 0.05) and inconclusive tests. "
                 "Use realistic conversion rates (1–8%) and visitor counts (1k–50k per variant)."),
            ],
        },
    },
}


def build_tool_use_2_prompts() -> tuple[int, int]:
    os.makedirs(BASE_2, exist_ok=True)
    total_dirs = 0
    total_prompts = 0

    for domain, subdomains in TOOL_DOMAINS_2.items():
        for subdomain, info in subdomains.items():
            dirpath = os.path.join(BASE_2, domain, subdomain)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for filename, angle_prompt in info["angles"]:
                prompt = build_prompt(domain, subdomain, info, filename, angle_prompt)
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  tool_use_2/{domain}/{subdomain}/prompts.txt ({len(lines)} prompts)")

    return total_dirs, total_prompts


# ---------------------------------------------------------------------------
# JSON QA — context / input / output extraction examples
# ---------------------------------------------------------------------------

JSON_QA_FORMAT = (
    "Format for each example (use EXACTLY this layout):\n"
    "Context: <1–3 sentences>\n"
    'Input: {"question": "<natural language question>"}\n'
    'Output: {"answer": "<extracted value>"}\n\n'
    "Separate examples with a single blank line. "
    "Answers must be copied verbatim from the context (no paraphrase). "
    "Use varied sentence structures and topics."
)

JSON_QA_MULTI_FORMAT = (
    "Format for each example (use EXACTLY this layout):\n"
    "Context: <1–3 sentences>\n"
    'Input: {"extract": ["field1", "field2", ...]}\n'
    "Output: {\"field1\": \"value1\", \"field2\": value2, ...}\n\n"
    "Separate examples with a single blank line. "
    "Values must be copied verbatim from the context. "
    "Use realistic, varied contexts."
)

JSON_QA = {
    "simple_facts": {
        "who_subject": [
            ("who_person.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a person's name or role. "
             "Contexts should be 1–2 sentences about everyday events (work, school, sport, travel). "
             "Questions ask 'Who ...' and answers are a name or role (e.g. 'the teacher', 'Maria')."),
            ("who_animal.corpus",
             "Generate 15 JSON QA extraction examples where the answer identifies an animal or creature. "
             "Contexts involve pets, wildlife, or farm animals in simple scenarios. "
             "Questions ask 'Who/What ...' and answers are animal names or types."),
        ],
        "what_object": [
            ("what_item.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a physical object or item. "
             "Contexts describe someone using, finding, or losing an everyday object. "
             "Questions ask 'What did X use/find/buy/bring?' and answers are the object name."),
            ("what_food.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a food or drink item. "
             "Contexts describe meals, cooking, or ordering at a restaurant. "
             "Questions ask 'What did X eat/order/make?' and answers are food/drink items."),
        ],
        "where_location": [
            ("where_place.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a place or location. "
             "Contexts describe someone going to or being at a location (park, office, city, store). "
             "Questions ask 'Where ...' and answers are location names extracted from the context."),
            ("where_direction.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a direction or position. "
             "Contexts describe spatial relationships (under the table, on the left, behind the door). "
             "Questions ask 'Where is/was X?' and answers are positional phrases."),
        ],
        "when_time": [
            ("when_clock.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a time of day or clock time. "
             "Contexts mention specific times (at 3pm, after midnight, early in the morning). "
             "Questions ask 'When/What time ...' and answers are the time phrase from the context."),
            ("when_date.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a date, day, or year. "
             "Contexts include dates for events, appointments, or historical facts. "
             "Questions ask 'When/What day/year ...' and answers are date values."),
        ],
        "how_many": [
            ("count_objects.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a count or quantity. "
             "Contexts mention specific numbers of items, people, or units. "
             "Questions ask 'How many ...' and answers are numbers extracted from the context."),
            ("measure_amount.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a measurement or amount. "
             "Contexts mention distances, weights, volumes, prices, or durations. "
             "Questions ask 'How much/far/long/heavy ...' and answers include the unit."),
        ],
        "color_attributes": [
            ("color.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a color. "
             "Contexts describe objects, clothing, or nature using specific color words. "
             "Questions ask 'What color is/was ...' and answers are single color words."),
            ("size_shape_temp.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a size, shape, or temperature. "
             "Contexts describe physical properties (large, round, freezing, tiny). "
             "Questions ask 'How big/What shape/How hot ...' and answers are the descriptor."),
        ],
    },
    "multi_field": {
        "person_profile": [
            ("name_age_city.corpus",
             "Generate 15 JSON QA extraction examples that extract a person's name, age, and city simultaneously. "
             "Contexts are 2–3 sentences describing a person. "
             'Input asks to extract ["name", "age", "city"]. '
             "Output values must be copied verbatim from the context. "
             + JSON_QA_MULTI_FORMAT),
            ("name_job_company.corpus",
             "Generate 15 JSON QA extraction examples that extract a person's name, job title, and company. "
             "Contexts describe a professional in a work setting. "
             'Input asks to extract ["name", "job", "company"]. '
             + JSON_QA_MULTI_FORMAT),
        ],
        "event_details": [
            ("event_date_location.corpus",
             "Generate 15 JSON QA extraction examples that extract an event's name, date, and location. "
             "Contexts describe conferences, parties, sports games, or ceremonies. "
             'Input asks to extract ["event", "date", "location"]. '
             + JSON_QA_MULTI_FORMAT),
            ("event_participants_outcome.corpus",
             "Generate 15 JSON QA extraction examples that extract who participated and what the outcome was. "
             "Contexts describe competitions, meetings, or negotiations. "
             'Input asks to extract ["participants", "outcome"]. '
             + JSON_QA_MULTI_FORMAT),
        ],
        "product_info": [
            ("product_name_price_brand.corpus",
             "Generate 15 JSON QA extraction examples that extract a product's name, price, and brand. "
             "Contexts describe buying or reviewing consumer products. "
             'Input asks to extract ["product", "price", "brand"]. '
             + JSON_QA_MULTI_FORMAT),
            ("product_category_rating.corpus",
             "Generate 15 JSON QA extraction examples that extract product category, rating, and availability. "
             "Contexts are short product review or shopping scenarios. "
             'Input asks to extract ["category", "rating", "in_stock"]. '
             + JSON_QA_MULTI_FORMAT),
        ],
        "transaction": [
            ("amount_sender_recipient.corpus",
             "Generate 15 JSON QA extraction examples that extract a transaction amount, sender, and recipient. "
             "Contexts describe payments, transfers, or purchases between named parties. "
             'Input asks to extract ["amount", "sender", "recipient"]. '
             + JSON_QA_MULTI_FORMAT),
            ("date_method_status.corpus",
             "Generate 15 JSON QA extraction examples that extract a transaction date, payment method, and status. "
             "Contexts describe financial transactions with specific details. "
             'Input asks to extract ["date", "method", "status"]. '
             + JSON_QA_MULTI_FORMAT),
        ],
    },
    "negation_conditional": {
        "did_not": [
            ("who_did_not.corpus",
             "Generate 15 JSON QA extraction examples where the answer is who did NOT do something. "
             "Contexts describe a group where one person abstained or was excluded. "
             "Questions ask 'Who did not ...' and answers are the name(s) that did not participate."),
            ("what_was_not.corpus",
             "Generate 15 JSON QA extraction examples where the answer is something that was absent or not used. "
             "Contexts describe a situation that explicitly mentions what was missing or unavailable. "
             "Questions ask 'What was not ...' and answers are the absent item or attribute."),
        ],
        "conditional_outcome": [
            ("if_then.corpus",
             "Generate 15 JSON QA extraction examples where the answer is the outcome of a condition. "
             "Contexts contain explicit if/when/unless clauses with stated consequences. "
             "Questions ask 'What happens if ...' or 'What will X do if ...' and answers are the consequence."),
            ("required_condition.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a requirement or prerequisite. "
             "Contexts state what must happen before something else can occur. "
             "Questions ask 'What is required to ...' and answers are the stated condition."),
        ],
    },
    "reading_comprehension": {
        "cause_effect": [
            ("why_cause.corpus",
             "Generate 15 JSON QA extraction examples where the answer explains why something happened. "
             "Contexts are 2–3 sentences with a clear cause-and-effect relationship. "
             "Questions ask 'Why did ...' and answers are the cause phrase from the context."),
            ("what_caused.corpus",
             "Generate 15 JSON QA extraction examples where the answer is the event that triggered an outcome. "
             "Contexts describe chain-reaction or causal scenarios. "
             "Questions ask 'What caused ...' and answers are extracted causal phrases."),
        ],
        "sequence_events": [
            ("first_last.corpus",
             "Generate 15 JSON QA extraction examples where the answer is the first or last event in a sequence. "
             "Contexts describe a series of 3–5 ordered steps or events. "
             "Questions ask 'What happened first/last?' and answers are the event descriptions."),
            ("before_after.corpus",
             "Generate 15 JSON QA extraction examples where the answer is what happened before or after a given event. "
             "Contexts describe temporal sequences. "
             "Questions ask 'What happened before/after X?' and answers are extracted event phrases."),
        ],
        "comparison": [
            ("which_more.corpus",
             "Generate 15 JSON QA extraction examples where the answer identifies which of two things has more of a property. "
             "Contexts compare two people, objects, or places on a measurable attribute (taller, faster, cheaper). "
             "Questions ask 'Which is ...' and answers are the entity name."),
            ("by_how_much.corpus",
             "Generate 15 JSON QA extraction examples where the answer is a numeric difference or ratio. "
             "Contexts state explicit numbers for two compared items. "
             "Questions ask 'By how much ...' or 'How much more ...' and answers include the value and unit."),
        ],
        "inference": [
            ("simple_inference.corpus",
             "Generate 15 JSON QA extraction examples requiring one simple inference step. "
             "Contexts imply a fact not stated verbatim (e.g. 'She grabbed her umbrella' → it was raining). "
             "Questions ask about the implied fact; answers are concise inferred values."),
            ("pronoun_resolution.corpus",
             "Generate 15 JSON QA extraction examples where the answer requires resolving a pronoun to its referent. "
             "Contexts introduce 2–3 characters, then use 'he', 'she', or 'they'. "
             "Questions ask 'Who does he/she/they refer to?' and answers are the resolved name."),
        ],
    },
}

JSON_QA_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus", "json_qa")

# ---------------------------------------------------------------------------
# json_qa_2 — longer contexts, array output, nested extraction
# Lives in corpus/json_qa_2/. Requests 20 examples per file.
# ---------------------------------------------------------------------------

JSON_QA_2_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus", "json_qa_2")

JSON_QA_ARRAY_FORMAT = (
    "Format for each example (use EXACTLY this layout):\n"
    "Context: <3–6 sentences>\n"
    'Input: {"question": "<natural language question>"}\n'
    'Output: {"answer": ["item1", "item2", ...]}\n\n'
    "Separate examples with a single blank line. "
    "List items must be copied verbatim from the context. "
    "Use varied topics and sentence structures."
)

JSON_QA_NESTED_FORMAT = (
    "Format for each example (use EXACTLY this layout):\n"
    "Context: <3–6 sentences>\n"
    'Input: {"extract": "<what to extract>"}\n'
    "Output: { <nested JSON object with 2–3 levels of nesting> }\n\n"
    "Separate examples with a single blank line. "
    "Values must be copied verbatim from the context. "
    "Nested keys should be snake_case."
)

JSON_QA_2 = {
    "paragraph_extraction": {
        "news_article": [
            ("news_who_what_where.corpus",
             "Generate 20 JSON QA extraction examples using 4–6 sentence news-style paragraphs as context. "
             "Each paragraph covers a distinct event (product launch, political announcement, sports result, natural disaster). "
             "Questions ask for a single fact (who, what, where, when, how many). "
             "Use the single-field format: Output: {\"answer\": \"...\"}. "
             "Contexts should feel like real news leads."),
            ("news_multi_field.corpus",
             "Generate 20 JSON QA multi-field extraction examples using 4–6 sentence news paragraphs. "
             'Input asks to extract 3–5 fields (e.g. ["who", "what", "location", "date", "outcome"]). '
             "Output is a flat JSON object with those fields. "
             "Use the multi-field format. Vary topics: business, politics, science, sports."),
        ],
        "biography": [
            ("bio_single_fact.corpus",
             "Generate 20 JSON QA extraction examples using 4–6 sentence biographical paragraphs. "
             "Each paragraph describes a real-sounding person (name, birthplace, career, achievement). "
             "Questions ask for one fact. Output: {\"answer\": \"...\"}. "
             "Use the single-field format with varied question phrasings."),
            ("bio_multi_field.corpus",
             "Generate 20 JSON QA multi-field extraction examples from biographical paragraphs. "
             'Input asks to extract ["name", "birth_year", "nationality", "profession", "known_for"]. '
             "Output is a flat JSON object. Use the multi-field format. "
             "Make the bios feel like encyclopedia entries."),
        ],
        "incident_report": [
            ("incident_single.corpus",
             "Generate 20 JSON QA extraction examples using 4–6 sentence incident or accident report paragraphs. "
             "Scenarios: workplace accidents, vehicle collisions, data breaches, system outages. "
             "Questions ask for one fact (time, location, cause, severity). Output: {\"answer\": \"...\"}. "
             "Use the single-field format."),
            ("incident_multi_field.corpus",
             "Generate 20 JSON QA multi-field extraction examples from incident reports. "
             'Input asks to extract ["incident_type", "date", "location", "cause", "severity", "resolved"]. '
             "Output is a flat JSON object. Use the multi-field format."),
        ],
        "product_review": [
            ("review_single.corpus",
             "Generate 20 JSON QA extraction examples using 4–6 sentence product review paragraphs. "
             "Reviews cover electronics, appliances, software, and clothing. "
             "Questions ask for one fact (rating, product name, pros, cons, verdict). Output: {\"answer\": \"...\"}. "
             "Use the single-field format."),
            ("review_multi_field.corpus",
             "Generate 20 JSON QA multi-field extraction examples from product reviews. "
             'Input asks to extract ["product", "rating", "main_pro", "main_con", "recommended"]. '
             "Output is a flat JSON object. Use the multi-field format."),
        ],
    },
    "array_extraction": {
        "list_entities": [
            ("extract_people.corpus",
             "Generate 20 JSON QA examples where the answer is a list of people's names. "
             "Contexts (3–5 sentences) mention multiple named individuals in a scenario (meeting, event, team). "
             'Questions: \'Who was present?\', \'Who signed the agreement?\'. '
             "Output: {\"answer\": [\"Name1\", \"Name2\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
            ("extract_locations.corpus",
             "Generate 20 JSON QA examples where the answer is a list of places or locations. "
             "Contexts describe trips, delivery routes, or multi-city events. "
             'Questions: \'Which cities were visited?\', \'Where did the shipment stop?\'. '
             "Output: {\"answer\": [\"City1\", \"City2\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
        ],
        "list_items": [
            ("extract_ingredients.corpus",
             "Generate 20 JSON QA examples where the answer is a list of ingredients or materials. "
             "Contexts describe recipes, manufacturing processes, or supply lists. "
             "Output: {\"answer\": [\"item1\", \"item2\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
            ("extract_steps.corpus",
             "Generate 20 JSON QA examples where the answer is an ordered list of steps or actions. "
             "Contexts describe procedures, instructions, or event sequences. "
             'Questions: \'What steps were taken?\', \'List the actions in order.\'. '
             "Output: {\"answer\": [\"step1\", \"step2\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
        ],
        "extract_numbers": [
            ("extract_quantities.corpus",
             "Generate 20 JSON QA examples where the answer is a list of numeric values with units. "
             "Contexts mention multiple measurements, prices, counts, or durations. "
             'Questions: \'What quantities were ordered?\', \'List all prices mentioned.\'. '
             "Output: {\"answer\": [\"12kg\", \"$45.00\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
            ("extract_dates.corpus",
             "Generate 20 JSON QA examples where the answer is a list of dates or times. "
             "Contexts describe schedules, timelines, or historical event sequences. "
             'Questions: \'What dates are mentioned?\', \'When did each phase start?\'. '
             "Output: {\"answer\": [\"2024-03-01\", \"2024-06-15\", ...]}. "
             + JSON_QA_ARRAY_FORMAT),
        ],
    },
    "nested_extraction": {
        "person_with_address": [
            ("person_address_nested.corpus",
             "Generate 20 JSON QA examples where the output is a nested person object. "
             "Contexts (3–5 sentences) describe a person including their contact details and location. "
             'Input: {"extract": "person details"}. '
             'Output: {"name": "...", "age": N, "contact": {"email": "...", "phone": "..."}, "address": {"street": "...", "city": "...", "country": "..."}}. '
             + JSON_QA_NESTED_FORMAT),
            ("person_employment.corpus",
             "Generate 20 JSON QA examples with nested person + employment details. "
             "Contexts describe someone's professional background. "
             'Input: {"extract": "employment details"}. '
             'Output: {"person": {"name": "...", "age": N}, "job": {"title": "...", "company": "...", "start_year": N, "salary": N}}. '
             + JSON_QA_NESTED_FORMAT),
        ],
        "order_with_items": [
            ("order_nested.corpus",
             "Generate 20 JSON QA examples with a nested order object. "
             "Contexts describe a purchase with multiple line items, shipping, and payment info. "
             'Input: {"extract": "order details"}. '
             'Output: {"order_id": "...", "customer": "...", "items": [{"name": "...", "qty": N, "price": N}], "totals": {"subtotal": N, "shipping": N, "total": N}}. '
             + JSON_QA_NESTED_FORMAT),
            ("shipment_nested.corpus",
             "Generate 20 JSON QA examples with a nested shipment tracking object. "
             "Contexts describe a delivery with carrier info, status, and tracking events. "
             'Input: {"extract": "shipment details"}. '
             'Output: {"tracking_number": "...", "carrier": "...", "status": "...", "events": [{"date": "...", "location": "...", "status": "..."}]}. '
             + JSON_QA_NESTED_FORMAT),
        ],
        "event_with_participants": [
            ("event_nested.corpus",
             "Generate 20 JSON QA examples with a nested event object. "
             "Contexts describe a meeting, conference, or ceremony with participants and outcomes. "
             'Input: {"extract": "event details"}. '
             'Output: {"event": "...", "date": "...", "location": "...", "organizer": "...", "participants": ["...", "..."], "outcome": "..."}. '
             + JSON_QA_NESTED_FORMAT),
            ("contract_nested.corpus",
             "Generate 20 JSON QA examples with a nested contract or agreement object. "
             "Contexts describe a business deal with parties, terms, and dates. "
             'Input: {"extract": "contract details"}. '
             'Output: {"parties": {"buyer": "...", "seller": "..."}, "terms": {"value": N, "currency": "...", "duration_months": N}, "signed_date": "...", "status": "..."}. '
             + JSON_QA_NESTED_FORMAT),
        ],
    },
}


def build_json_qa_2_prompts() -> tuple[int, int]:
    os.makedirs(JSON_QA_2_BASE, exist_ok=True)
    total_dirs = 0
    total_prompts = 0

    for category, subcategories in JSON_QA_2.items():
        for subcategory, angles in subcategories.items():
            dirpath = os.path.join(JSON_QA_2_BASE, category, subcategory)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for filename, angle_prompt in angles:
                prompt = f"Category: {category}/{subcategory}\n\n{angle_prompt}"
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  json_qa_2/{category}/{subcategory}/prompts.txt ({len(lines)} prompts)")

    return total_dirs, total_prompts


def build_json_qa_prompt(category: str, subcategory: str, angle_prompt: str) -> str:
    if "multi_field" in category or JSON_QA_MULTI_FORMAT in angle_prompt:
        fmt = ""  # format already embedded in angle_prompt for multi_field
    else:
        fmt = "\n\n" + JSON_QA_FORMAT
    return f"Category: {category}/{subcategory}\n\n{angle_prompt}{fmt}"


def build_json_qa_prompts() -> tuple[int, int]:
    os.makedirs(JSON_QA_BASE, exist_ok=True)
    total_dirs = 0
    total_prompts = 0

    for category, subcategories in JSON_QA.items():
        for subcategory, angles in subcategories.items():
            dirpath = os.path.join(JSON_QA_BASE, category, subcategory)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for filename, angle_prompt in angles:
                prompt = build_json_qa_prompt(category, subcategory, angle_prompt)
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  json_qa/{category}/{subcategory}/prompts.txt ({len(lines)} prompts)")

    return total_dirs, total_prompts


# ---------------------------------------------------------------------------

def build_prompt(domain: str, subdomain: str, info: dict, filename: str, angle_prompt: str) -> str:
    return (
        f"Domain: {domain}/{subdomain}\n"
        f"Available Tools: {info['tools']}\n"
        f"Call Schema: {info['call_schema']}\n"
        f"Response Schema: {info['response_schema']}\n\n"
        f"{angle_prompt}"
    )


def main():
    os.makedirs(BASE, exist_ok=True)
    total_dirs = 0
    total_prompts = 0

    print("Building tool_use prompts...")
    for domain, subdomains in TOOL_DOMAINS.items():
        for subdomain, info in subdomains.items():
            dirpath = os.path.join(BASE, domain, subdomain)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for filename, angle_prompt in info["angles"]:
                prompt = build_prompt(domain, subdomain, info, filename, angle_prompt)
                # One-line format: filename<space>prompt (prompt has no newlines)
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  tool_use/{domain}/{subdomain}/prompts.txt ({len(lines)} prompts)")

    print("\nBuilding tool_use_2 prompts...")
    t2_dirs, t2_prompts = build_tool_use_2_prompts()
    total_dirs += t2_dirs
    total_prompts += t2_prompts

    print("\nBuilding json_qa prompts...")
    qa_dirs, qa_prompts = build_json_qa_prompts()
    total_dirs += qa_dirs
    total_prompts += qa_prompts

    print("\nBuilding json_qa_2 prompts...")
    qa2_dirs, qa2_prompts = build_json_qa_2_prompts()
    total_dirs += qa2_dirs
    total_prompts += qa2_prompts

    print(f"\nDone! Created {total_dirs} directories with {total_prompts} total prompts.")


if __name__ == "__main__":
    main()
