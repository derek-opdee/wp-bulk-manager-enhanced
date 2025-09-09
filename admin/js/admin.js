/**
 * WP Bulk Manager Admin JavaScript
 */

(function($) {
    'use strict';
    
    $(document).ready(function() {
        
        // Initialize tabs
        $('.nav-tab').on('click', function(e) {
            e.preventDefault();
            
            var tabId = $(this).attr('href');
            
            $('.nav-tab').removeClass('nav-tab-active');
            $(this).addClass('nav-tab-active');
            
            $('.tab-content').removeClass('active');
            $(tabId).addClass('active');
        });
        
        // Variable tag insertion
        $('.variable-tag').on('click', function() {
            var variable = $(this).data('variable');
            var $editor = $('#template-content');
            
            // Insert at cursor position
            var cursorPos = $editor[0].selectionStart;
            var v = $editor.val();
            var textBefore = v.substring(0, cursorPos);
            var textAfter = v.substring(cursorPos, v.length);
            
            $editor.val(textBefore + '{' + variable + '}' + textAfter);
            
            // Set cursor position after inserted text
            var newPos = cursorPos + variable.length + 2;
            $editor[0].setSelectionRange(newPos, newPos);
            $editor.focus();
        });
        
        // Live preview
        $('#template-content, #preview-replacements input').on('keyup change', function() {
            updatePreview();
        });
        
        function updatePreview() {
            var template = $('#template-content').val();
            var replacements = {};
            
            $('#preview-replacements input').each(function() {
                var key = $(this).data('variable');
                var value = $(this).val();
                if (value) {
                    replacements[key] = value;
                }
            });
            
            // Simple replacement for preview
            var preview = template;
            $.each(replacements, function(key, value) {
                var regex = new RegExp('\\{' + key + '\\}', 'g');
                preview = preview.replace(regex, value);
            });
            
            $('#preview-output').html(preview);
        }
        
        // Bulk action handler
        $('#bulk-action-form').on('submit', function(e) {
            e.preventDefault();
            
            var selectedSites = [];
            $('.site-checkbox:checked').each(function() {
                selectedSites.push($(this).val());
            });
            
            if (selectedSites.length === 0) {
                alert('Please select at least one site.');
                return;
            }
            
            var action = $('#bulk-action-selector').val();
            if (!action) {
                alert('Please select an action.');
                return;
            }
            
            // Show progress
            var $progress = $('<div class="queue-status"><div class="queue-progress"><div class="queue-progress-bar" style="width: 0%;"></div></div></div>');
            $(this).after($progress);
            
            // Simulate progress
            var progress = 0;
            var progressInterval = setInterval(function() {
                progress += 10;
                $progress.find('.queue-progress-bar').css('width', progress + '%');
                
                if (progress >= 100) {
                    clearInterval(progressInterval);
                    $progress.fadeOut(function() {
                        $(this).remove();
                    });
                }
            }, 500);
        });
        
        // Site search/filter
        $('#site-search').on('keyup', function() {
            var searchTerm = $(this).val().toLowerCase();
            
            $('.site-card').each(function() {
                var siteName = $(this).find('h4').text().toLowerCase();
                var domain = $(this).find('.site-domain').text().toLowerCase();
                
                if (siteName.includes(searchTerm) || domain.includes(searchTerm)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });
        
        // Template validation
        $('#save-template').on('click', function() {
            var content = $('#template-content').val();
            
            // Check for balanced braces
            var openBraces = (content.match(/\{/g) || []).length;
            var closeBraces = (content.match(/\}/g) || []).length;
            
            if (openBraces !== closeBraces) {
                alert('Template has mismatched braces. Please check your spintax syntax.');
                return false;
            }
        });
        
        // Auto-save draft
        var autoSaveTimer;
        $('#template-content').on('keyup', function() {
            clearTimeout(autoSaveTimer);
            
            autoSaveTimer = setTimeout(function() {
                // Save to localStorage
                var templateData = {
                    content: $('#template-content').val(),
                    name: $('#template-name').val(),
                    type: $('#template-type').val()
                };
                
                localStorage.setItem('wp_bulk_manager_draft', JSON.stringify(templateData));
                
                // Show saved indicator
                $('.auto-save-status').text('Draft saved').fadeIn().delay(2000).fadeOut();
            }, 2000);
        });
        
        // Restore draft
        var draft = localStorage.getItem('wp_bulk_manager_draft');
        if (draft) {
            draft = JSON.parse(draft);
            if (confirm('Restore previous draft?')) {
                $('#template-content').val(draft.content);
                $('#template-name').val(draft.name);
                $('#template-type').val(draft.type);
            }
        }
        
    });
    
})(jQuery);