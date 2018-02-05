window._wapiq = window._wapiq || [];
_wapiq.push(function(W) {
    window.wistiaUploader = new W.Uploader({
        accessToken: "47ec67f7053e1c4f8cb01eac2e8103f12510932dcbff694b5690d5c011c0c835",
        dropIn: "wistia_uploader",
        projectId: "ucxz9sy1gn",
        theme: 'light_background',
        embedCodeOptions: {
            playerColor: "6b0b0b",
            videoFoam: true
        }
    });
    wistiaUploader.bind("uploadembeddable", function(file, media, embedCode, oembedResponse) {
        document.getElementById("video_id").value = media.id
        document.getElementById("video_duration").value = media.duration
        document.getElementById("video_thumbnail").value = media.thumbnail.url
        document.getElementById("video_html").value = embedCode
    });
    wistiaUploader.bind('uploadsuccess', function(file, media) {
        document.getElementById("confirm_upload").style.display = "block";
    });
});