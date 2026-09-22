const url = "https://drive.usercontent.google.com/download?id=1WgJAVFGjfXQQ4q0GtYiI63nxD_D6-7a5";
fetch(url).then(response => {
    const newHeaders = new Headers(response.headers);
    console.log("Before:", newHeaders.get("cross-origin-embedder-policy"));
    newHeaders.delete("cross-origin-embedder-policy");
    console.log("After:", newHeaders.get("cross-origin-embedder-policy"));
});
