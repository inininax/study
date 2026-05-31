# Next App
## Sass Support
- Install
```shell
yarn add -D sass
```

- Customizing Sass Options
```javascript
// next.config.js
const path = require('path');
module.exports = {
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
}
```

- Sass Variables (variables.module.scss)
```scss
$primary-color: #64FF00;
export{
  primaryColor: $primary-color
}
```

- pages/_app.js
```javascript
import variables from '../styles/variables.module.scss'
export default function MyApp({Component, pageProps}) {
  return (
    <Layout color={variables.primaryColor}>
      <Component {...pageProps} />
    </Layout>
  )
}
```