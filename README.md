# nn.Demo
front-end flask app for cxr pneumonia neural-net

this makes a 'multipart/form-data' post request with ['file']:image_file or dcm_file

the response json format : 
```
{
  "apiVersion": "< 0.5.1", 
  "appName": "api.nn.Demo", 
  "dxList": [
    "pneumonia", 
    "other opacity (not specified)"
  ], 
  "exit_code": 0, 
  "img_base64": base 64 encoded image,
  "model_id": model_id, 
  "prediction": {
    "prediction": [
      Dx, 
      Probability
    ], 
    "prediction_all": [
      [
        "pneumonia", 
        pna_prob
      ], 
      [
        "other opacity (not specified)", 
        abn_prob
      ]
    ]
  }, 
  "saliency": base_64_encoded_saliency_image, 
  "training_id": training id
}
```

<!-- ![demo screenshot](static_files/screenshot%20demo%200.jpg) -->
<img src="static_files/screenshot%20demo%200.jpg" alt="demo screenshot" width="360"/>
