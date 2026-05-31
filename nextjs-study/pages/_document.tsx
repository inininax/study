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
          <link rel="icon" href="/favicon.ico" />
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