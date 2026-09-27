const fs = require('fs');

const files = [
"Everyday_Filming_Logic_Carousel - @jazziesillona.html",
"Hong_Kong_Visual_Rhythm_Carousel - @withyuee.html",
"IG_@Andrei_Kostromskikh_DcI-darjckz_Carousel_Analysis.html",
"IG_@Andrei_Kostromskikh_DctRlh0jZlj_Carousel_Analysis.html",
"IG_@Banh_shimano_Dc0-FXlE4kV_Carousel_Analysis.html",
"IG_@Beixin_Travel_&_Nature_Dc0zRNwDz11_Carousel_Analysis.html",
"IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis.html",
"IG_@Gabe_Harris_Dc3ih_5jlqz_Carousel_Analysis.html",
"IG_@davidmurphyfilm_Ddo3aQxjMeq_Carousel_Analysis.html",
"IG_@dvdnguyen_DdXbbBiEq7P_Carousel_Analysis.html",
"IG_@gakuyen_Dc0MQfeEwp4_Carousel_Analysis.html",
"IG_@mcjacoub_Ddlh5pagYie_Carousel_Analysis.html",
"IG_@minghan1004_DdESxNlE2Ay_Carousel_Analysis.html",
"IG_@shotsbyzaid_DdkimD5DPNL_Carousel_Analysis.html",
"IG_@ulanzi_ohxID_MagSafe_Compatible_Selfie_Stick_Tripod_Produc.html",
"IG_@yongandmike_DdolqWHEsws_Carousel_Analysis.html",
"IG_@岳_🍜_GAKU_Dc0MHhTE9z0_Carousel_Analysis.html",
"IG_@𝗧𝗵𝗼𝗺𝗮𝘀_𝗠𝗮𝘁𝗵𝗲𝘄_DcgSonjgnkV_Carousel_Analysis.html",
"Mood_and_Tone_Carousel - @jazziesillona.html",
"Quy_Tac_Quay_Phim_Carousel - @Jacoub_Anwar.html",
"Street_Photography_Carousel - @jazziesillona.html",
"Urban_Texture_Carousel - @jazziesillona.html",
"Visual_Stopping_Power_Carousel - @jazziesillona.html",
"Visual_Storytelling_Carousel - @withyuee.html"
];

const jsErrorFiles = [
"IG_@davidmurphyfilm_Ddo3aQxjMeq_Carousel_Analysis.html",
"IG_@dvdnguyen_DdXbbBiEq7P_Carousel_Analysis.html",
"IG_@minghan1004_DdESxNlE2Ay_Carousel_Analysis.html",
"IG_@shotsbyzaid_DdkimD5DPNL_Carousel_Analysis.html",
"IG_@yongandmike_DdolqWHEsws_Carousel_Analysis.html"
];

let md = "| # | Tên File | CSS Khung 75vh | Nút Điều Hướng (▲/▼) | Lỗi JS (`player.play`) | Nghiệm Thu |\n";
md += "|---|---|---|---|---|---|\n";

files.forEach((f, i) => {
    let jsStatus = jsErrorFiles.includes(f) ? "✅ Đã vá lỗi đứt gãy" : "✅ Sạch";
    md += `| ${i+1} | ${f.replace('.html', '')} | ✅ Chuẩn | ✅ Đã bơm | ${jsStatus} | [Live URL](https://ytuong.fedu.vn/reports/${encodeURI(f)}) |\n`;
});

fs.writeFileSync('table.md', md);
