# Next App
## Styled-components
- Install
```shell
yarn add styled-components
yarn add -D @types/styled-components babel-plugin-styled-components
```

- next.config.js
```javascript
module.exports = {
  compiler: {
    // ssr and displayName are configured by default
    styledComponents: true,
  },
}
```

- .babelrc
```json
{
  "presets": [
    "next/babel"
  ],
  "plugins": [
    [
      "styled-components",
      {
        "ssr": true
      }
    ]
  ]
}
```

- index.tsx
```typescript jsx
import styled from 'styled-components'

const Title = styled.h1`
  font-size: 50px;
  color: ${({ theme }) => theme.colors.primary};
`

export default function Home() {
  return <Title>My page</Title>
}
```

- _app.tsx
```typescript jsx
import { AppProps } from "next/app";
import { createGlobalStyle, ThemeProvider } from "styled-components";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <GlobalStyle />
      <ThemeProvider theme={theme}>
        <Component {...pageProps} />
      </ThemeProvider>
    </>
  );
};

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
`;

const theme = {
  colors: {
    primary: "#0070f3",
  },
};
```

- _document.tsx
```typescript jsx
import Document, { DocumentContext, Head, Html, Main, NextScript } from "next/document";
import { ServerStyleSheet } from "styled-components";

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="ko">
        <Head>
          <meta charSet="utf-8" />
          <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no" />
          <meta name="robots" content="index,nofollow" />
          <meta name="description" content="" />
          <meta property="og:title" content="" />
          <meta property="og:url" content="" />
          <meta property="og:image" content="" />
          <meta property="og:description" content="" />
          <meta name="twitter:card" content="summary" />
          <meta name="twitter:title" content="" />
          <meta name="twitter:url" content="" />
          <meta name="twitter:image" content="" />
          <meta name="twitter:description" content="" />
          <title>Admin App</title>
        </Head>
        <body>
        <Main />
        <NextScript />
        </body>
      </Html>
    );
  }

  static async getInitialProps(ctx: DocumentContext) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp:
            (App: any) =>
              (props: any) =>
                sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: (
          <>
            {initialProps.styles}
            {sheet.getStyleElement()}
          </>
        ),
      };
    } finally {
      sheet.seal();
    }
  }
}
```