KT.panel.list.registerPage("changesets",{extra_params:[{hash_id:"env_id",init_func:function(){var a=$.bbq.getState("env_id");if(a){env_select.set_selected(a)}else{$.bbq.pushState({env_id:env_select.get_selected_env()})}}}]});$(document).ready(function(){env_select.click_callback=function(a){$.bbq.pushState({env_id:a});$("#search_form").trigger("submit")}});var changeset_page={signal_rename:function(b,a){KT.panel.list.refresh("changeset_"+b,$("#changeset").attr("data-ajax_url"))}};