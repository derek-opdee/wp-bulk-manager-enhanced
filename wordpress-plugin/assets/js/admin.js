/**
 * WP Bulk Manager Admin JavaScript
 */

(function($) {
    'use strict';

    $(document).ready(function() {
        
        // API Key generation
        $('#generate-api-key, #regenerate-api-key').on('click', function(e) {
            e.preventDefault();
            
            if (!confirm('Generate a new API key? The old key will stop working immediately.')) {
                return;
            }
            
            var $button = $(this);
            $button.prop('disabled', true).text('Generating...');
            
            $.post(wpbm_ajax.ajax_url, {
                action: 'wpbm_generate_api_key',
                nonce: wpbm_ajax.nonce
            })
            .done(function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert('Failed to generate API key. Please try again.');
                    $button.prop('disabled', false).text('Generate New Key');
                }
            })
            .fail(function() {
                alert('An error occurred. Please try again.');
                $button.prop('disabled', false).text('Generate New Key');
            });
        });
        
        // Copy API key to clipboard
        $('.wpbm-copy-api-key').on('click', function(e) {
            e.preventDefault();
            
            var apiKey = $(this).data('api-key');
            var $temp = $('<input>');
            $('body').append($temp);
            $temp.val(apiKey).select();
            document.execCommand('copy');
            $temp.remove();
            
            var $button = $(this);
            var originalText = $button.text();
            $button.text('Copied!');
            
            setTimeout(function() {
                $button.text(originalText);
            }, 2000);
        });
        
        // Test API connection
        $('#test-api-connection').on('click', function(e) {
            e.preventDefault();
            
            var $button = $(this);
            var $status = $('#api-connection-status');
            
            $button.prop('disabled', true).text('Testing...');
            $status.html('<span class="spinner is-active"></span> Testing connection...');
            
            $.get(wpbm_ajax.site_url + '/wp-json/wpbm/v1/content?limit=1', {
                headers: {
                    'X-API-Key': $('#wpbm-test-api-key').val()
                }
            })
            .done(function(response) {
                $status.html('<span style="color: green;">✓ Connection successful!</span>');
                $button.prop('disabled', false).text('Test Connection');
            })
            .fail(function(xhr) {
                var message = 'Connection failed';
                if (xhr.status === 401) {
                    message = 'Invalid API key';
                } else if (xhr.status === 403) {
                    message = 'Access denied (check IP whitelist)';
                }
                
                $status.html('<span style="color: red;">✗ ' + message + '</span>');
                $button.prop('disabled', false).text('Test Connection');
            });
        });
        
        // Clear logs
        $('#clear-activity-logs').on('click', function(e) {
            e.preventDefault();
            
            if (!confirm('Clear all activity logs? This cannot be undone.')) {
                return;
            }
            
            $.post(wpbm_ajax.ajax_url, {
                action: 'wpbm_clear_logs',
                nonce: wpbm_ajax.nonce
            })
            .done(function(response) {
                if (response.success) {
                    location.reload();
                }
            });
        });
        
        // Auto-refresh activity log
        if ($('.wpbm-activity-log-table').length) {
            setInterval(function() {
                $.get(wpbm_ajax.ajax_url, {
                    action: 'wpbm_get_recent_activity',
                    nonce: wpbm_ajax.nonce
                })
                .done(function(response) {
                    if (response.success && response.data) {
                        updateActivityLog(response.data);
                    }
                });
            }, 30000); // Refresh every 30 seconds
        }
        
        function updateActivityLog(logs) {
            var $tbody = $('.wpbm-activity-log-table tbody');
            var html = '';
            
            if (logs.length === 0) {
                html = '<tr><td colspan="4">No activity logged yet.</td></tr>';
            } else {
                $.each(logs, function(i, log) {
                    html += '<tr>';
                    html += '<td>' + escapeHtml(log.timestamp) + '</td>';
                    html += '<td>' + escapeHtml(log.event) + '</td>';
                    html += '<td>' + escapeHtml(log.ip) + '</td>';
                    html += '<td>' + escapeHtml(JSON.stringify(log.details)) + '</td>';
                    html += '</tr>';
                });
            }
            
            $tbody.html(html);
        }
        
        function escapeHtml(text) {
            var map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            
            return text.replace(/[&<>"']/g, function(m) { return map[m]; });
        }
        
    });

})(jQuery);