# Phosphor-icon-vue-component

Browse a folder with SVG files from the `Phosphor Icons` library to mine them and (if desired) create an import system for the icons to easily use them in a Vue.js component


Starts the command with the path to the svg folder to process as argument.

`python3 manage_svg.py path/to/folder`


If you use the easy import creation feature, the icon names to use will be the svg file names without the extension. (example: for a file named `cross.svg`, the icon name will simply be `cross`)

The import path in the `MyIcon.vue` component of the `importSvg.ts` function must be changed to match the path you provided in the script.

The `MyIcon.vue` component is designed to work with Tailwind, however, it is easily modified so as not to depend on it.

How call `MyIcon.vue` component in a component parent ?

```
<MyIconVue
        :icon="cross"
        size="sm"
        :stroke-color="stroke-black"
        :stroke-width="lg"
        fill-color="fill-white"
      />
```
