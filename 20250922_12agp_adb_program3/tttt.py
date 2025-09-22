def ocr_check(img, target="music", show=True):
    if img is None or img.size == 0:
        return False

    res_en = reader_en.readtext(img, detail=1, paragraph=False)
    res_ko = reader_ko.readtext(img, detail=1, paragraph=False)
    results = res_en + res_ko

    texts = [text for _, text, conf in results if conf >= conf_print]
    print("인식된 텍스트:", texts)

    if show:
        vis = _draw_boxes(img, results)
        h, w = vis.shape[:2]
        vis_small = cv2.resize(vis, (w//3, h//3), interpolation=cv2.INTER_AREA)
        cv2.imshow("ocr", vis_small); cv2.waitKey(1)

    if target == "audio":
        found = set()
        for _, text, _ in results:
            up = re.sub(r"\s+", "", text.upper())
            for kw in audio_keyword:
                if kw in up:
                    found.add(kw)
        return found.issuperset(set(audio_keyword))

    elif target == "home":
        full_ko = "".join([t for _, t, _ in res_ko]) 
        # home_keyword 전체가 포함되어야 True
        return all(kw in full_ko for kw in home_keyword)

    elif target == "menu":
        full_ko = "".join([t for _, t, _ in res_ko]) 
        # menu_keyword 전체가 포함되어야 True
        return all(kw in full_ko for kw in menu_keyword)



    else:
        return False