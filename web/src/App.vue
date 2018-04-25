<template>
  <div class="example-drag">
    <div class="upload">
      <ul v-if="files.length">
        <li v-for="file in files" :key="file.id">
          <span>{{file.name}}</span> -
          <span>{{file.size}}</span> -
          <span v-if="file.error">{{file.error}}</span>
          <span v-else-if="file.success">success</span>
          <span v-else-if="file.active">active</span>
          <span v-else-if="file.active">active</span>
          <span v-else></span>
        </li>
      </ul>
      <ul v-else>
        <td colspan="7">
          <div class="text-center p-5">
            <h4>Drop files anywhere to upload<br/>or</h4>
            <label for="file" class="btn btn-lg btn-primary">Select Zip File</label>
          </div>
        </td>
      </ul>

      <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active">
    		<h3>Drop file to upload</h3>
      </div>

      <div class="example-btn">
        <file-upload
          class="btn btn-primary"
          post-action="/upload"
          :multiple="false"
          :drop="true"
          :drop-directory="false"
          v-model="files"
          ref="upload">
          <i class="fa fa-plus"></i>
          Select Zip file
        </file-upload>
        <button type="button" class="btn btn-success" v-if="!$refs.upload || !$refs.upload.active" @click.prevent="onUpload">
          <i class="fa fa-arrow-up" aria-hidden="true"></i>
          Start Upload
        </button>
        <button type="button" class="btn btn-danger"  v-else @click.prevent="$refs.upload.active = false">
          <i class="fa fa-stop" aria-hidden="true"></i>
          Stop Upload
        </button>
      </div>
      <GetLog class="panel panel-info" ref="log">
      </GetLog>
    </div>
  </div>
</template>
<style>
.example-drag label.btn {
  margin-bottom: 0;
  margin-right: 1rem;
}


.example-drag .drop-active {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 9999;
  opacity: .6;
  text-align: center;
  background: #000;
}

.example-drag .drop-active h3 {
  margin: -.5em 0 0;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
  font-size: 40px;
  color: #fff;
  padding: 0;
}
</style>

<script>
/* eslint-disable */
import FileUpload from 'vue-upload-component'
import GetLog from './components/GetLog.vue'
export default {
  components: {
    FileUpload,
    GetLog
  },
  methods:{
    onUpload() {
      this.$refs.upload.active = true
      this.$refs.log.clear()
    }
  },
  data() {
    return {
      files: [],
    }
  }
}
</script>