<template>
 <div>
    <pre class='log'>
        {{LogData}}
    </pre>
    <hr>
    <a v-bind:href='OutputZipUrl'>{{OutputZipUrl}}</a>
 </div>
</template>

<style>
.log {
    height: auto;
    max-height: 400px;
    overflow: auto;
    background-color: #eeeeee;
    word-break: normal !important;
    word-wrap: normal !important;
    white-space: pre !important;
}
</style>

<script>
import axios from 'axios';
import VueTimers from 'vue-timers/mixin'

export default{
    mixins: [VueTimers],
    data() {
        return {
            LogData: [],
            OutputZipUrl: 'No result'
        }
    },
    timers: {
        log: { time: 3000, autostart: true, repeat:true }
    },
    methods: {
        clear() {
            this.LogData = ''
            this.OutputZipUrl = ''
        },
        log () {
            // console.log('Hello world')
            axios.get(`/GetLog`)
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.LogData = response.data
                    this.OutputZipUrl = this.LogData["zipfile"]
                    // console.log(obj['zipfile'])
                    // console.log(obj['log'])
                    // this.OutputZipUrl = obj['zipfile']
                    // this.LogData = obj['log']
                })
                .catch(e => {
                    this.errors.push(e)
                })
        }
    }
}
</script>

