extends PanelContainer

func set_entries(entries: Array) -> void:
    $Content/Entries.text = "\n".join(entries)

func add_entry(text: String) -> void:
    $Content/Entries.text += ("\n" if $Content/Entries.text else "") + text
