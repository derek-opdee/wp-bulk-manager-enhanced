#!/usr/bin/env python3
"""
WP Bulk Manager GUI - macOS Desktop Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from wpbm_manager import WPBulkManager, ContentProcessor
import threading


class WPBulkManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WP Bulk Manager")
        self.root.geometry("1200x800")
        
        # Initialize manager
        self.manager = WPBulkManager()
        
        # Create menu bar
        self.create_menu()
        
        # Create main layout
        self.create_layout()
        
        # Load sites
        self.refresh_sites()
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Site", command=self.show_add_site_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Templates", command=self.show_templates_window)
        tools_menu.add_command(label="Variables", command=self.show_variables_window)
    
    def create_layout(self):
        """Create main application layout"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sites tab
        self.sites_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sites_frame, text="Sites")
        self.create_sites_tab()
        
        # Content tab
        self.content_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.content_frame, text="Create Content")
        self.create_content_tab()
        
        # Bulk Operations tab
        self.bulk_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bulk_frame, text="Bulk Operations")
        self.create_bulk_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_sites_tab(self):
        """Create sites management tab"""
        # Sites list
        list_frame = ttk.Frame(self.sites_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for sites
        columns = ('ID', 'Name', 'Domain', 'Status', 'Last Sync')
        self.sites_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        # Configure columns
        self.sites_tree.column('#0', width=0, stretch=False)
        self.sites_tree.column('ID', width=50)
        self.sites_tree.column('Name', width=200)
        self.sites_tree.column('Domain', width=300)
        self.sites_tree.column('Status', width=100)
        self.sites_tree.column('Last Sync', width=150)
        
        # Headers
        for col in columns:
            self.sites_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.sites_tree.yview)
        self.sites_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.sites_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = ttk.Frame(self.sites_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Site", command=self.show_add_site_dialog).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Test Connection", command=self.test_selected_site).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_sites).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_selected_site).pack(side='left', padx=5)
    
    def create_content_tab(self):
        """Create content creation tab"""
        # Site selection
        select_frame = ttk.LabelFrame(self.content_frame, text="Select Sites", padding=10)
        select_frame.pack(fill='x', padx=10, pady=10)
        
        self.site_checkboxes_frame = ttk.Frame(select_frame)
        self.site_checkboxes_frame.pack(fill='both', expand=True)
        
        # Content form
        form_frame = ttk.LabelFrame(self.content_frame, text="Content Details", padding=10)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky='w', pady=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(form_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        # Content type
        ttk.Label(form_frame, text="Type:").grid(row=1, column=0, sticky='w', pady=5)
        self.type_var = tk.StringVar(value='page')
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, values=['post', 'page'], width=20)
        type_combo.grid(row=1, column=1, sticky='w', pady=5)
        
        # Status
        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar(value='draft')
        status_combo = ttk.Combobox(form_frame, textvariable=self.status_var, values=['draft', 'publish', 'private'], width=20)
        status_combo.grid(row=2, column=1, sticky='w', pady=5)
        
        # Content
        ttk.Label(form_frame, text="Content:").grid(row=3, column=0, sticky='nw', pady=5)
        self.content_text = scrolledtext.ScrolledText(form_frame, width=60, height=15)
        self.content_text.grid(row=3, column=1, sticky='ew', pady=5)
        
        # Variables hint
        var_hint = ttk.Label(form_frame, text="Use variables: {location}, {service}, {service_plural}")
        var_hint.grid(row=4, column=1, sticky='w')
        
        # SEO Fields
        seo_frame = ttk.LabelFrame(form_frame, text="SEO Settings", padding=5)
        seo_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)
        
        ttk.Label(seo_frame, text="SEO Title:").grid(row=0, column=0, sticky='w', pady=2)
        self.seo_title_var = tk.StringVar()
        ttk.Entry(seo_frame, textvariable=self.seo_title_var, width=50).grid(row=0, column=1, sticky='ew', pady=2)
        
        ttk.Label(seo_frame, text="SEO Description:").grid(row=1, column=0, sticky='w', pady=2)
        self.seo_desc_var = tk.StringVar()
        ttk.Entry(seo_frame, textvariable=self.seo_desc_var, width=50).grid(row=1, column=1, sticky='ew', pady=2)
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        seo_frame.columnconfigure(1, weight=1)
        
        # Create button
        ttk.Button(form_frame, text="Create Content", command=self.create_content).grid(row=6, column=0, columnspan=2, pady=20)
    
    def create_bulk_tab(self):
        """Create bulk operations tab"""
        # Template selection
        template_frame = ttk.LabelFrame(self.bulk_frame, text="Template & Variables", padding=10)
        template_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(template_frame, text="Select Template:").pack(anchor='w')
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, width=50)
        self.template_combo.pack(fill='x', pady=5)
        
        # Variables
        var_frame = ttk.LabelFrame(self.bulk_frame, text="Variable Values", padding=10)
        var_frame.pack(fill='x', padx=10, pady=10)
        
        # Locations
        ttk.Label(var_frame, text="Locations (one per line):").pack(anchor='w')
        self.locations_text = scrolledtext.ScrolledText(var_frame, width=50, height=5)
        self.locations_text.pack(fill='x', pady=5)
        self.locations_text.insert('1.0', "Brisbane\nSydney\nMelbourne\nPerth")
        
        # Services
        ttk.Label(var_frame, text="Services (JSON format):").pack(anchor='w')
        self.services_text = scrolledtext.ScrolledText(var_frame, width=50, height=5)
        self.services_text.pack(fill='x', pady=5)
        default_services = {
            "painting": {"singular": "painting service", "plural": "painting services"},
            "plumbing": {"singular": "plumbing service", "plural": "plumbing services"}
        }
        self.services_text.insert('1.0', json.dumps(default_services, indent=2))
        
        # Preview
        preview_frame = ttk.LabelFrame(self.bulk_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, width=60, height=10)
        self.preview_text.pack(fill='both', expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.bulk_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_bulk_content).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate & Create", command=self.execute_bulk_create).pack(side='left', padx=5)
    
    def refresh_sites(self):
        """Refresh sites list"""
        # Clear existing items
        for item in self.sites_tree.get_children():
            self.sites_tree.delete(item)
        
        # Get sites
        sites = self.manager.get_sites('all')
        
        # Add to tree
        for site in sites:
            self.sites_tree.insert('', 'end', values=(
                site['id'],
                site['name'],
                site['domain'],
                site['status'],
                site['last_sync'] or 'Never'
            ))
        
        # Update site checkboxes
        self.update_site_checkboxes()
    
    def update_site_checkboxes(self):
        """Update site selection checkboxes"""
        # Clear existing checkboxes
        for widget in self.site_checkboxes_frame.winfo_children():
            widget.destroy()
        
        # Create new checkboxes
        self.site_vars = {}
        sites = self.manager.get_sites('active')
        
        for site in sites:
            var = tk.BooleanVar()
            self.site_vars[site['id']] = var
            cb = ttk.Checkbutton(
                self.site_checkboxes_frame,
                text=f"{site['name']} ({site['domain']})",
                variable=var
            )
            cb.pack(anchor='w', pady=2)
    
    def show_add_site_dialog(self):
        """Show dialog to add new site"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Site")
        dialog.geometry("500x300")
        
        # Form fields
        ttk.Label(dialog, text="Site Name:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Site URL:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        url_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=url_var, width=40).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="API Key:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        key_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=key_var, width=40, show='*').grid(row=2, column=1, padx=10, pady=5)
        
        # Instructions
        instructions = ttk.Label(
            dialog,
            text="Generate the API key in WordPress Admin → Settings → Bulk Manager",
            wraplength=450
        )
        instructions.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Buttons
        def add_site():
            name = name_var.get()
            url = url_var.get()
            api_key = key_var.get()
            
            if not all([name, url, api_key]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            self.status_bar.config(text="Testing connection...")
            
            # Add site in background thread
            def add_task():
                success = self.manager.add_site(name, url, api_key)
                
                self.root.after(0, lambda: self.handle_add_site_result(success, name, dialog))
            
            threading.Thread(target=add_task).start()
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Site", command=add_site).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
    
    def handle_add_site_result(self, success, name, dialog):
        """Handle add site result"""
        if success:
            self.status_bar.config(text=f"Successfully added site: {name}")
            dialog.destroy()
            self.refresh_sites()
        else:
            self.status_bar.config(text="Failed to add site")
            messagebox.showerror("Error", "Failed to add site. Please check the URL and API key.")
    
    def test_selected_site(self):
        """Test connection to selected site"""
        selection = self.sites_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a site to test")
            return
        
        site_id = self.sites_tree.item(selection[0])['values'][0]
        site = self.manager.get_site(site_id)
        api_key = self.manager.get_site_api_key(site_id)
        
        if self.manager.test_connection(site['url'], api_key):
            messagebox.showinfo("Success", f"Successfully connected to {site['name']}")
        else:
            messagebox.showerror("Error", f"Failed to connect to {site['name']}")
    
    def remove_selected_site(self):
        """Remove selected site"""
        selection = self.sites_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a site to remove")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this site?"):
            # TODO: Implement site removal
            messagebox.showinfo("Not Implemented", "Site removal not yet implemented")
    
    def create_content(self):
        """Create content on selected sites"""
        # Get selected sites
        selected_sites = [site_id for site_id, var in self.site_vars.items() if var.get()]
        
        if not selected_sites:
            messagebox.showwarning("No Sites", "Please select at least one site")
            return
        
        # Prepare content data
        content_data = {
            'title': self.title_var.get(),
            'content': self.content_text.get('1.0', 'end-1c'),
            'type': self.type_var.get(),
            'status': self.status_var.get()
        }
        
        # Add SEO data if provided
        seo_data = {}
        if self.seo_title_var.get():
            seo_data['title'] = self.seo_title_var.get()
        if self.seo_desc_var.get():
            seo_data['description'] = self.seo_desc_var.get()
        
        if seo_data:
            content_data['seo'] = seo_data
        
        # Create content in background
        self.status_bar.config(text="Creating content...")
        
        def create_task():
            results = self.manager.create_content(selected_sites, content_data)
            self.root.after(0, lambda: self.show_creation_results(results))
        
        threading.Thread(target=create_task).start()
    
    def show_creation_results(self, results):
        """Show content creation results"""
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        self.status_bar.config(text=f"Created content on {success_count}/{total_count} sites")
        
        # Show detailed results
        result_text = "Content Creation Results:\n\n"
        for result in results:
            if result['success']:
                result_text += f"✅ {result['site_name']}: Created successfully\n"
                result_text += f"   URL: {result['permalink']}\n\n"
            else:
                result_text += f"❌ {result['site_name']}: {result['error']}\n\n"
        
        # Show in a dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Creation Results")
        dialog.geometry("600x400")
        
        text = scrolledtext.ScrolledText(dialog, width=60, height=20)
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert('1.0', result_text)
        text.config(state='disabled')
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def preview_bulk_content(self):
        """Preview bulk content generation"""
        # Get template
        template = "<!-- wp:heading -->\n<h1>{service|capitalize} in {location}</h1>\n<!-- /wp:heading -->\n\n<!-- wp:paragraph -->\n<p>Welcome to our {service} in {location}.</p>\n<!-- /wp:paragraph -->"
        
        # Get variables
        locations = [loc.strip() for loc in self.locations_text.get('1.0', 'end-1c').split('\n') if loc.strip()]
        
        try:
            services = json.loads(self.services_text.get('1.0', 'end-1c'))
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in services field")
            return
        
        # Generate preview
        processor = ContentProcessor()
        preview = "Content Preview:\n\n"
        
        # Show first example
        if locations and services:
            location = locations[0]
            service_key = list(services.keys())[0]
            service_data = services[service_key]
            
            replacements = {
                'location': location,
                'service': service_data['singular'],
                'service_plural': service_data['plural']
            }
            
            content = processor.process(template, replacements)
            preview += f"Example for {location} - {service_data['singular']}:\n"
            preview += "-" * 50 + "\n"
            preview += content + "\n\n"
            
            # Show variation count
            total_variations = len(locations) * len(services)
            preview += f"Total variations to be created: {total_variations}"
        
        self.preview_text.delete('1.0', 'end')
        self.preview_text.insert('1.0', preview)
    
    def execute_bulk_create(self):
        """Execute bulk content creation"""
        # Get selected sites
        selected_sites = [site_id for site_id, var in self.site_vars.items() if var.get()]
        
        if not selected_sites:
            messagebox.showwarning("No Sites", "Please select at least one site")
            return
        
        # TODO: Implement bulk creation with progress dialog
        messagebox.showinfo("Not Implemented", "Bulk creation with variables not yet fully implemented")
    
    def show_templates_window(self):
        """Show templates management window"""
        # TODO: Implement templates window
        messagebox.showinfo("Not Implemented", "Templates management not yet implemented")
    
    def show_variables_window(self):
        """Show variables management window"""
        # TODO: Implement variables window
        messagebox.showinfo("Not Implemented", "Variables management not yet implemented")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = WPBulkManagerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()