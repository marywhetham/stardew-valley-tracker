def get_links_from_table(table, desc_name):
    tr_with_source = get_tr_from_table(table, desc_name)
    return tr_with_source.select("a") if tr_with_source is not None else None

def get_tr_from_table(table, desc_name):
    tr_with_source = next(
        (tr for tr in table.find_all("tr") if tr.find("td", string=lambda text: text and desc_name in text)),
        None
    )
    return tr_with_source if tr_with_source is not None else None