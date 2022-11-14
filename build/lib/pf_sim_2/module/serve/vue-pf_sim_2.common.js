module.exports =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "fae3");
/******/ })
/************************************************************************/
/******/ ({

/***/ "0613":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_0_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_0_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_0_2_style_css_vue_type_style_index_0_prod_module_true_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("6c02");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_0_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_0_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_0_2_style_css_vue_type_style_index_0_prod_module_true_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_0_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_0_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_0_2_style_css_vue_type_style_index_0_prod_module_true_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (default from non-harmony) */ __webpack_require__.d(__webpack_exports__, "default", function() { return _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_0_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_0_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_0_2_style_css_vue_type_style_index_0_prod_module_true_lang_css___WEBPACK_IMPORTED_MODULE_0___default.a; });
 

/***/ }),

/***/ "6c02":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin
module.exports = {"btn":"style_btn_1gQXH","btnClick":"style_btnClick_1HT7j style_btn_1gQXH","btnChange":"style_btnChange_32CE5 style_btn_1gQXH"};

/***/ }),

/***/ "ec27":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_1_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_1_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_1_2_style_css_vue_type_style_index_0_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("fe80");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_1_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_1_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_1_2_style_css_vue_type_style_index_0_prod_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_1_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_1_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_1_2_style_css_vue_type_style_index_0_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* unused harmony reexport * */


/***/ }),

/***/ "fae3":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, "install", function() { return /* reexport */ install; });

// CONCATENATED MODULE: ./node_modules/@vue/cli-service/lib/commands/build/setPublicPath.js
// This file is imported into lib/wc client bundles.

if (typeof window !== 'undefined') {
  var currentScript = window.document.currentScript
  if (false) { var getCurrentScript; }

  var src = currentScript && currentScript.src.match(/(.+\/)[^/]+\.js(\?.*)?$/)
  if (src) {
    __webpack_require__.p = src[1] // eslint-disable-line
  }
}

// Indicate to webpack that this file can be concatenated
/* harmony default export */ var setPublicPath = (null);

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js?{"cacheDirectory":"node_modules/.cache/vue-loader","cacheIdentifier":"73570d97-vue-loader-template"}!./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./src/components/CustomWidget/template.html?vue&type=template&id=a7cc851c&
var render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',[_c('v-btn',{class:_vm.$style.btnClick,on:{"click":_vm.triggerClick}},[_vm._v("Custom click")]),_c('v-btn',{class:_vm.$style.btnChange,on:{"click":_vm.triggerChange}},[_vm._v("Custom change")])],1)}
var staticRenderFns = []


// CONCATENATED MODULE: ./src/components/CustomWidget/template.html?vue&type=template&id=a7cc851c&

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js??ref--13-0!./node_modules/thread-loader/dist/cjs.js!./node_modules/babel-loader/lib!./node_modules/eslint-loader??ref--14-0!./src/components/CustomWidget/script.js?vue&type=script&lang=js&
/* harmony default export */ var scriptvue_type_script_lang_js_ = ({
  name: 'CustomWidget',
  props: {
    attribute_name: {
      type: String
    },
    js_attr_name: {
      type: String
    }
  },
  methods: {
    triggerClick() {
      this.$emit('click');
    },
    triggerChange() {
      this.$emit('change');
    }
  }
});
// CONCATENATED MODULE: ./src/components/CustomWidget/script.js?vue&type=script&lang=js&
 /* harmony default export */ var CustomWidget_scriptvue_type_script_lang_js_ = (scriptvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./src/components/CustomWidget/style.css?vue&type=style&index=0&prod&module=true&lang=css&
var stylevue_type_style_index_0_prod_module_true_lang_css_ = __webpack_require__("0613");

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
/* globals __VUE_SSR_CONTEXT__ */

// IMPORTANT: Do NOT use ES2015 features in this file (except for modules).
// This module is a runtime utility for cleaner component module output and will
// be included in the final webpack user bundle.

function normalizeComponent(
  scriptExports,
  render,
  staticRenderFns,
  functionalTemplate,
  injectStyles,
  scopeId,
  moduleIdentifier /* server only */,
  shadowMode /* vue-cli only */
) {
  // Vue.extend constructor export interop
  var options =
    typeof scriptExports === 'function' ? scriptExports.options : scriptExports

  // render functions
  if (render) {
    options.render = render
    options.staticRenderFns = staticRenderFns
    options._compiled = true
  }

  // functional template
  if (functionalTemplate) {
    options.functional = true
  }

  // scopedId
  if (scopeId) {
    options._scopeId = 'data-v-' + scopeId
  }

  var hook
  if (moduleIdentifier) {
    // server build
    hook = function (context) {
      // 2.3 injection
      context =
        context || // cached call
        (this.$vnode && this.$vnode.ssrContext) || // stateful
        (this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext) // functional
      // 2.2 with runInNewContext: true
      if (!context && typeof __VUE_SSR_CONTEXT__ !== 'undefined') {
        context = __VUE_SSR_CONTEXT__
      }
      // inject component styles
      if (injectStyles) {
        injectStyles.call(this, context)
      }
      // register component module identifier for async chunk inferrence
      if (context && context._registeredComponents) {
        context._registeredComponents.add(moduleIdentifier)
      }
    }
    // used by ssr in case component is cached and beforeCreate
    // never gets called
    options._ssrRegister = hook
  } else if (injectStyles) {
    hook = shadowMode
      ? function () {
          injectStyles.call(
            this,
            (options.functional ? this.parent : this).$root.$options.shadowRoot
          )
        }
      : injectStyles
  }

  if (hook) {
    if (options.functional) {
      // for template-only hot-reload because in that case the render fn doesn't
      // go through the normalizer
      options._injectStyles = hook
      // register for functional component in vue file
      var originalRender = options.render
      options.render = function renderWithStyleInjection(h, context) {
        hook.call(context)
        return originalRender(h, context)
      }
    } else {
      // inject component registration as beforeCreate hook
      var existing = options.beforeCreate
      options.beforeCreate = existing ? [].concat(existing, hook) : [hook]
    }
  }

  return {
    exports: scriptExports,
    options: options
  }
}

// CONCATENATED MODULE: ./src/components/CustomWidget/index.vue








function injectStyles (context) {
  
  this["$style"] = (stylevue_type_style_index_0_prod_module_true_lang_css_["default"].locals || stylevue_type_style_index_0_prod_module_true_lang_css_["default"])

}

/* normalize component */

var component = normalizeComponent(
  CustomWidget_scriptvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  injectStyles,
  null,
  null
  
)

/* harmony default export */ var CustomWidget = (component.exports);
// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js?{"cacheDirectory":"node_modules/.cache/vue-loader","cacheIdentifier":"73570d97-vue-loader-template"}!./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./src/components/FileDatabase/template.html?vue&type=template&id=0d504104&
var templatevue_type_template_id_0d504104_render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('v-container',{staticClass:"fill-height",attrs:{"fluid":""}},[_c('v-row',{staticClass:"fill-height flex-nowrap"},[_c('v-col',{staticClass:"fill-height d-flex flex-column",staticStyle:{"border-right":"1px solid grey"},attrs:{"cols":"12","sm":"4"}},[_c('v-toolbar',{staticClass:"flex-grow-0",attrs:{"dense":"","flat":""}},[_c('v-text-field',{attrs:{"label":"Search","prepend-icon":"mdi-magnify"},model:{value:(_vm.searchQuery),callback:function ($$v) {_vm.searchQuery=$$v},expression:"searchQuery"}}),_c('v-btn',{staticClass:"ml-2 align-self-start",attrs:{"outlined":"","small":"","icon":""},on:{"click":_vm.newFile}},[_c('v-icon',[_vm._v(" mdi-plus")])],1)],1),_c('v-divider'),_c('v-list',[_c('v-list-item-group',{attrs:{"value":_vm.value ? _vm.value.id : ''},on:{"change":_vm.selectFile}},[_vm._l((_vm.files),function(file,index){return [(_vm.searchMatch(file))?_c('v-list-item',{key:file.id,attrs:{"value":file.id}},[_c('div',{staticClass:"d-flex flex-column align-start py-2"},[_c('v-icon',{staticClass:"pr-2"},[_vm._v(" "+_vm._s(_vm.iconFromType(file.type))+" ")]),(file.dateUploaded)?_c('span',{staticClass:"text-caption font-weight-thin"},[_vm._v(" "+_vm._s(new Date(file.dateUploaded).toLocaleDateString())+" ")]):_vm._e(),_c('span',{staticClass:"text-caption font-weight-thin"},[_vm._v(" "+_vm._s(file.category)+" ")])],1),_c('v-list-item-content',{staticClass:"pl-2"},[_c('v-list-item-title',[_vm._v(_vm._s(file.name))]),_c('v-list-item-subtitle',[_vm._v(" "+_vm._s(file.description)+" ")])],1),_c('v-icon',{staticClass:"ml-2",on:{"click":function($event){return _vm.removeFile(file.id)}}},[_vm._v(" mdi-delete ")])],1):_vm._e(),_c('v-divider',{key:("divider-" + index)})]})],2)],1)],1),_c('v-col',{attrs:{"cols":"12","sm":"8"}},[(!_vm.value)?_c('div',{staticClass:"font-weight-medium flex-column d-flex justify-center align-center\n        fill-height"},[(_vm.hasFiles)?_c('span',[_vm._v("No file selected. Select one or ")]):_c('span',[_vm._v("No files in database ")]),_c('a',{on:{"click":_vm.newFile}},[_vm._v(" (Add a file) ")])]):_c('v-container',{staticClass:"fill-height"},[_c('v-row',{staticClass:"justify-start flex-nowrap align-self-start"},[_c('v-col',{staticClass:"align-center",attrs:{"cols":"12","sm":"7"}},[_c('v-text-field',{attrs:{"label":"Name","outlined":""},model:{value:(_vm.formContent.name),callback:function ($$v) {_vm.$set(_vm.formContent, "name", $$v)},expression:"formContent.name"}}),_c('DragAndDropFiles',{staticClass:"flex-grow-1 text-caption mx-auto",attrs:{"disabled":_vm.formContent.useLocalFile,"file":_vm.file},on:{"uploaded":_vm.uploaded}}),_c('v-divider',{staticStyle:{"margin":"1rem"}}),_c('v-checkbox',{attrs:{"label":"Specify a local file on the server"},model:{value:(_vm.formContent.useLocalFile),callback:function ($$v) {_vm.$set(_vm.formContent, "useLocalFile", $$v)},expression:"formContent.useLocalFile"}}),_c('v-text-field',{attrs:{"label":"File path on server","disabled":!_vm.formContent.useLocalFile,"outlined":""},model:{value:(_vm.formContent.localFile),callback:function ($$v) {_vm.$set(_vm.formContent, "localFile", $$v)},expression:"formContent.localFile"}}),(_vm.error)?_c('v-alert',{attrs:{"dense":"","outlined":"","type":"error"}},[_vm._v(_vm._s(_vm.error))]):_vm._e()],1),_c('v-col',{attrs:{"cols":"12","sm":"5"}},[_c('v-select',{attrs:{"label":"Category","items":_vm.fileCategories,"filled":""},model:{value:(_vm.formContent.category),callback:function ($$v) {_vm.$set(_vm.formContent, "category", $$v)},expression:"formContent.category"}}),_c('v-row',{staticClass:"flex-nowrap"},[_c('v-list',{staticClass:"text-caption",attrs:{"dense":""}},[_c('v-list-item',[_c('v-list-item-content',[_c('v-list-item-subtitle',[_vm._v(" Origin")])],1)],1),_c('v-list-item',[_c('v-list-item-content',[_c('v-list-item-subtitle',[_vm._v(" Uploaded")])],1)],1),_c('v-list-item',[_c('v-list-item-content',[_c('v-list-item-subtitle',[_vm._v(" Modified")])],1)],1),_c('v-list-item',[_c('v-list-item-content',[_c('v-list-item-subtitle',[_vm._v(" Type")])],1)],1),_c('v-list-item',[_c('v-list-item-content',[_c('v-list-item-subtitle',[_vm._v(" Size")])],1)],1)],1),_c('v-list',{staticClass:"text-caption font-weight-bold",attrs:{"dense":""}},[_c('v-list-item',[_vm._v(" "+_vm._s(_vm.origin)+" ")]),_c('v-list-item',[_vm._v(" "+_vm._s(_vm.dateUploaded)+" ")]),_c('v-list-item',[_vm._v(" "+_vm._s(_vm.dateModified)+" ")]),_c('v-list-item',[_vm._v(" "+_vm._s(_vm.type)+" ")]),_c('v-list-item',[_vm._v(" "+_vm._s(_vm.size)+" ")])],1)],1)],1)],1),_c('v-row',{staticClass:"pa-4 grey lighten-3"},[_c('v-textarea',{attrs:{"label":"Description"},model:{value:(_vm.formContent.description),callback:function ($$v) {_vm.$set(_vm.formContent, "description", $$v)},expression:"formContent.description"}})],1),_c('v-row',{staticClass:"mt-auto pt-8"},[_c('v-btn',{staticClass:"white--text",attrs:{"text":"","elevation":"2","color":"grey"},on:{"click":_vm.downloadSelectedFile}},[_vm._v(" Download ")]),_c('v-btn',{staticClass:"ml-auto mr-2 white--text",attrs:{"text":"","elevation":"2","color":"red"},on:{"click":_vm.resetSelectedFile}},[_vm._v(" Cancel ")]),_c('v-btn',{attrs:{"text":"","elevation":"2","color":"primary"},on:{"click":_vm.save}},[_vm._v(" "+_vm._s('Save')+" ")])],1)],1)],1)],1)],1)}
var templatevue_type_template_id_0d504104_staticRenderFns = []


// CONCATENATED MODULE: ./src/components/FileDatabase/template.html?vue&type=template&id=0d504104&

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js?{"cacheDirectory":"node_modules/.cache/vue-loader","cacheIdentifier":"73570d97-vue-loader-template"}!./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./src/components/DragAndDropFiles/template.html?vue&type=template&id=1a0abc4c&
var templatevue_type_template_id_1a0abc4c_render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return (!_vm.file)?_c('div',{class:['dropZone', _vm.dragging ? 'dropZone-over' : '', _vm.disabled ? 'dropZone-disabled' : ''],on:{"dragenter":function($event){_vm.dragging = true},"dragleave":function($event){_vm.dragging = false}}},[_c('div',{staticClass:"dropZone-info",on:{"drag":_vm.onChange}},[_c('span',{staticClass:"dropZone-title"},[_vm._v("Drop file or click to upload")])]),_c('input',{attrs:{"disabled":_vm.disabled,"type":"file"},on:{"change":_vm.onChange}})]):_c('div',{class:['dropZone-uploaded', _vm.disabled ? 'dropZone-disabled' : '']},[_c('div',{staticClass:"dropZone-uploaded-info"},[_c('span',{staticClass:"dropZone-title"},[_vm._v("Uploaded")]),_c('button',{staticClass:"btn btn-primary removeFile",attrs:{"type":"button"},on:{"click":_vm.removeFile}},[_vm._v(" Remove File ")])])])}
var templatevue_type_template_id_1a0abc4c_staticRenderFns = []


// CONCATENATED MODULE: ./src/components/DragAndDropFiles/template.html?vue&type=template&id=1a0abc4c&

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js??ref--13-0!./node_modules/thread-loader/dist/cjs.js!./node_modules/babel-loader/lib!./node_modules/eslint-loader??ref--14-0!./src/components/DragAndDropFiles/script.js?vue&type=script&lang=js&
/* harmony default export */ var DragAndDropFiles_scriptvue_type_script_lang_js_ = ({
  name: 'DragNDropFiles',
  props: ['file', 'disabled'],
  data: () => ({
    dragging: false
  }),
  methods: {
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      this.dragging = false;
      if (this.disabled) {
        return;
      }
      if (!files.length) {
        return;
      }
      this.createFile(files[0]);
    },
    createFile(file) {
      this.$emit('uploaded', file);
    },
    removeFile() {
      this.createFile(undefined);
    }
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    }
  }
});
// CONCATENATED MODULE: ./src/components/DragAndDropFiles/script.js?vue&type=script&lang=js&
 /* harmony default export */ var components_DragAndDropFiles_scriptvue_type_script_lang_js_ = (DragAndDropFiles_scriptvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./src/components/DragAndDropFiles/style.css?vue&type=style&index=0&prod&lang=css&
var stylevue_type_style_index_0_prod_lang_css_ = __webpack_require__("ec27");

// CONCATENATED MODULE: ./src/components/DragAndDropFiles/index.vue






/* normalize component */

var DragAndDropFiles_component = normalizeComponent(
  components_DragAndDropFiles_scriptvue_type_script_lang_js_,
  templatevue_type_template_id_1a0abc4c_render,
  templatevue_type_template_id_1a0abc4c_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var DragAndDropFiles = (DragAndDropFiles_component.exports);
// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js??ref--13-0!./node_modules/thread-loader/dist/cjs.js!./node_modules/babel-loader/lib!./node_modules/eslint-loader??ref--14-0!./src/components/FileDatabase/script.js?vue&type=script&lang=js&

/* harmony default export */ var FileDatabase_scriptvue_type_script_lang_js_ = ({
  name: 'FileDatabase',
  components: {
    DragAndDropFiles: DragAndDropFiles
  },
  props: ['files', 'fileCategories', 'value', 'db-update', 'error', 'uploadFile', 'uploadLocalFile'],
  data() {
    return {
      searchQuery: '',
      fileStats: {},
      file: null,
      formContent: this.value || {}
    };
  },
  methods: {
    iconFromType(type) {
      if (type === 'zip') return 'mdi-folder-zip';
      if (type === 'folder') return 'mdi-folder';
      return 'mdi-file';
    },
    searchMatch(file) {
      if (this.searchQuery === '') return true;
      const regex = new RegExp(this.searchQuery);
      const checks = [file.name, file.description, file.category, file.type];
      for (var i = 0; i < checks.length; i++) {
        if (checks[i] && checks[i].search(regex) > -1) return true;
      }
      return false;
    },
    uploaded(file) {
      if (file) {
        this.fileStats = {
          size: file.size,
          origin: file.name,
          dateModified: file.lastModified,
          dateUploaded: Number(new Date()),
          type: file.type === 'application/zip' ? 'zip' : 'file'
        };
      } else {
        this.fileStats = {};
      }
      this.file = file;
    },
    selectFile(id) {
      console.log('selectFile', id);
      // this.trigger(this.dbUpdate, ['selectFile', id]);
    },

    removeFile(id) {
      console.log('removeFile', id);
      // this.trigger(this.dbUpdate, ['removeFile', id]);
    },

    downloadSelectedFile() {
      // this.trigger(this.dbUpdate, ['downloadSelectedFile', this.value.id]);
    },
    resetSelectedFile() {
      this.file = null;
      this.fileStats = {};
    },
    newFile() {
      this.fileStats = {};
      let name = 'unnamed file';
      let count = 1;
      const fileList = Object.values(this.files);
      while (fileList.find(file => file.name === name + ' ' + count)) {
        count++;
      }
      name = name + ' ' + count;
      this.$emit('input', {
        name,
        description: '',
        origin: null,
        size: null,
        dateModified: null,
        dateUploaded: null,
        type: null,
        gridSize: null,
        category: null
      });
    },
    save() {
      /*eslint no-unused-vars: ["error", { "ignoreRestSiblings": true }]*/
      const {
        useLocalFile,
        copyLocalFile,
        localFile,
        origin,
        dateModified,
        dateUploaded,
        type,
        size,
        ...formContent
      } = this.formContent;
      console.log('formContent', this.formContent);
      if (!useLocalFile && this.file) {
        var _this$value$id;
        this.$emit('uploadFile', {
          'entryId': (_this$value$id = this.value.id) !== null && _this$value$id !== void 0 ? _this$value$id : 'hi',
          'fileObj': this.file
        });
        this.resetSelectedFile();
      } else if (useLocalFile && localFile) {
        const fileMeta = {
          copyLocalFile,
          localFile,
          type: 'file'
        };
        this.$emit('uploadLocalFile', this.value.id, fileMeta);
      }
      this.$emit('input', {
        ...formContent
      });
    },
    cancel() {
      this.formContent = {
        ...(this.value || {})
      };
      this.resetSelectedFile();
    }
  },
  computed: {
    origin() {
      return this.fileStats.origin || this.formContent.origin;
    },
    dateUploaded() {
      const date = this.fileStats.dateUploaded || this.formContent.dateUploaded;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    dateModified() {
      const date = this.fileStats.dateModified || this.formContent.dateModified;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    type() {
      return this.fileStats.type || this.formContent.type;
    },
    size() {
      return this.fileStats.size || this.formContent.size;
    },
    hasFiles() {
      return Object.keys(this.files).length > 0;
    }
  },
  watch: {
    value() {
      this.cancel();
    }
  }
  // inject: ['set', 'trigger'],
});
// CONCATENATED MODULE: ./src/components/FileDatabase/script.js?vue&type=script&lang=js&
 /* harmony default export */ var components_FileDatabase_scriptvue_type_script_lang_js_ = (FileDatabase_scriptvue_type_script_lang_js_); 
// CONCATENATED MODULE: ./src/components/FileDatabase/index.vue





/* normalize component */

var FileDatabase_component = normalizeComponent(
  components_FileDatabase_scriptvue_type_script_lang_js_,
  templatevue_type_template_id_0d504104_render,
  templatevue_type_template_id_0d504104_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var FileDatabase = (FileDatabase_component.exports);
// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js?{"cacheDirectory":"node_modules/.cache/vue-loader","cacheIdentifier":"73570d97-vue-loader-template"}!./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./src/components/SimulationType/template.html?vue&type=template&id=5349140c&
var templatevue_type_template_id_5349140c_render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"pa-6 fill-height",staticStyle:{"overflow":"hide"}},[_c('v-container',{staticClass:"mt-8"},[_c('v-row',{staticClass:"justify-center"},[_c('div',{staticClass:"text-h4"},[_vm._v("What do you want to Model?")])]),_c('v-row',{staticClass:"justify-center"},[_c('div',{staticClass:"pt-2 text-subtitle-2 grey--text"},[_vm._v(" These shortcuts will fill in a few keys before you start. ")])]),_c('v-row',{staticClass:"justify-center align-center pt-6"},[_c('div',{staticClass:"text-h5 pr-4"},[_vm._v("Features")]),_c('v-checkbox',{staticClass:"pa-4",attrs:{"label":"Wells"},model:{value:(_vm.shortcuts.wells),callback:function ($$v) {_vm.$set(_vm.shortcuts, "wells", $$v)},expression:"shortcuts.wells"}}),_c('v-checkbox',{staticClass:"pa-4",attrs:{"label":"Climate"},model:{value:(_vm.shortcuts.climate),callback:function ($$v) {_vm.$set(_vm.shortcuts, "climate", $$v)},expression:"shortcuts.climate"}}),_c('v-checkbox',{staticClass:"pa-4",attrs:{"label":"Contaminants"},model:{value:(_vm.shortcuts.contaminants),callback:function ($$v) {_vm.$set(_vm.shortcuts, "contaminants", $$v)},expression:"shortcuts.contaminants"}})],1),_c('v-row',{staticClass:"justify-center align-center"},[_c('div',{staticClass:"text-h5 pr-4"},[_vm._v("Saturation")]),_c('v-radio-group',{staticClass:"pa-4",attrs:{"row":""},model:{value:(_vm.shortcuts.saturated),callback:function ($$v) {_vm.$set(_vm.shortcuts, "saturated", $$v)},expression:"shortcuts.saturated"}},[_c('v-radio',{attrs:{"value":"Variably Saturated","label":"Variably Saturated"}}),_c('v-radio',{attrs:{"value":"Fully Saturated","label":"Fully Saturated"}})],1)],1)],1)],1)}
var templatevue_type_template_id_5349140c_staticRenderFns = []


// CONCATENATED MODULE: ./src/components/SimulationType/template.html?vue&type=template&id=5349140c&

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js??ref--13-0!./node_modules/thread-loader/dist/cjs.js!./node_modules/babel-loader/lib!./node_modules/eslint-loader??ref--14-0!./src/components/SimulationType/script.js?vue&type=script&lang=js&
/* harmony default export */ var SimulationType_scriptvue_type_script_lang_js_ = ({
  name: 'SimulationType',
  props: ['shortcuts']
});
// CONCATENATED MODULE: ./src/components/SimulationType/script.js?vue&type=script&lang=js&
 /* harmony default export */ var components_SimulationType_scriptvue_type_script_lang_js_ = (SimulationType_scriptvue_type_script_lang_js_); 
// CONCATENATED MODULE: ./src/components/SimulationType/index.vue





/* normalize component */

var SimulationType_component = normalizeComponent(
  components_SimulationType_scriptvue_type_script_lang_js_,
  templatevue_type_template_id_5349140c_render,
  templatevue_type_template_id_5349140c_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var SimulationType = (SimulationType_component.exports);
// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js?{"cacheDirectory":"node_modules/.cache/vue-loader","cacheIdentifier":"73570d97-vue-loader-template"}!./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./src/components/NavigationDropDown/template.html?vue&type=template&id=502b3a14&
var templatevue_type_template_id_502b3a14_render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"d-flex align-center"},[_c('div',{staticClass:"pr-2"},[_c('v-btn',{attrs:{"outlined":"","small":"","icon":"","disabled":!_vm.canMoveBackward},on:{"click":_vm.moveBackward}},[_c('v-icon',[_vm._v(" mdi-chevron-left ")])],1)],1),_c('div',{staticStyle:{"padding-top":"26px"}},[_c('v-select',{staticStyle:{"width":"15em"},attrs:{"outlined":"","items":_vm.views,"value":_vm.value,"dense":""},on:{"change":function($event){return _vm.$emit('input', $event)}}})],1),_c('div',{staticClass:"pl-2"},[_c('v-btn',{attrs:{"outlined":"","small":"","icon":"","color":"primary","disabled":!_vm.canMoveForward},on:{"click":_vm.moveForward}},[_c('v-icon',[_vm._v(" mdi-chevron-right ")])],1)],1)])}
var templatevue_type_template_id_502b3a14_staticRenderFns = []


// CONCATENATED MODULE: ./src/components/NavigationDropDown/template.html?vue&type=template&id=502b3a14&

// CONCATENATED MODULE: ./node_modules/cache-loader/dist/cjs.js??ref--13-0!./node_modules/thread-loader/dist/cjs.js!./node_modules/babel-loader/lib!./node_modules/eslint-loader??ref--14-0!./src/components/NavigationDropDown/script.js?vue&type=script&lang=js&
/* harmony default export */ var NavigationDropDown_scriptvue_type_script_lang_js_ = ({
  name: 'NavigationDropDown',
  props: ['value', 'views'],
  data: () => ({}),
  computed: {
    canMoveForward() {
      const i = this.views.indexOf(this.value);
      return i !== -1 && i < this.views.length - 1;
    },
    canMoveBackward() {
      const i = this.views.indexOf(this.value);
      return i !== -1 && i > 0;
    }
  },
  methods: {
    moveBackward() {
      const i = this.views.indexOf(this.value);
      this.$emit('input', this.views[i - 1]);
    },
    moveForward() {
      const i = this.views.indexOf(this.value);
      this.$emit('input', this.views[i + 1]);
    }
  }
});
// CONCATENATED MODULE: ./src/components/NavigationDropDown/script.js?vue&type=script&lang=js&
 /* harmony default export */ var components_NavigationDropDown_scriptvue_type_script_lang_js_ = (NavigationDropDown_scriptvue_type_script_lang_js_); 
// CONCATENATED MODULE: ./src/components/NavigationDropDown/index.vue





/* normalize component */

var NavigationDropDown_component = normalizeComponent(
  components_NavigationDropDown_scriptvue_type_script_lang_js_,
  templatevue_type_template_id_502b3a14_render,
  templatevue_type_template_id_502b3a14_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var NavigationDropDown = (NavigationDropDown_component.exports);
// CONCATENATED MODULE: ./src/components/index.js




/* harmony default export */ var components = ({
  'yourCustomWidget': CustomWidget,
  'PfFileDatabase': FileDatabase,
  'PfSimulationType': SimulationType,
  'PfNavigationDropDown': NavigationDropDown
});
// CONCATENATED MODULE: ./src/use.js

function install(Vue) {
  Object.keys(components).forEach(name => {
    Vue.component(name, components[name]);
  });
}
;
// CONCATENATED MODULE: ./node_modules/@vue/cli-service/lib/commands/build/entry-lib-no-default.js




/***/ }),

/***/ "fe80":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ })

/******/ });
//# sourceMappingURL=vue-pf_sim_2.common.js.map