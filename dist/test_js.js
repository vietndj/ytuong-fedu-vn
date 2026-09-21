const currentSrc = "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/IG_%40%EC%A3%BC%EC%84%9C%EB%B0%A9_DcvmVl2hbuY_Video_by_ju_seobang/shot_01_mid.jpg";
const parsed = new URL(currentSrc);
const encodedPath = parsed.pathname.split('/').map(segment => encodeURIComponent(decodeURIComponent(segment))).join('/');
const safeUrl = `${parsed.origin}${encodedPath}${parsed.search}`;
console.log("currentSrc:", currentSrc);
console.log("safeUrl:   ", safeUrl);
console.log("Equal?     ", safeUrl === currentSrc);
