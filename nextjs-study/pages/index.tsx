import type { NextPage } from "next";
import Head from "next/head";
import styled from "styled-components";
import styles from "../styles/Home.module.scss";

const Home: NextPage = (): JSX.Element => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Main | Admin App</title>
      </Head>

      <main className={styles.main}>
        <Title>Styled Components</Title>
      </main>

      <footer className={styles.footer}>
        Footer
      </footer>
    </div>
  );
};

const Title = styled.h1`
  font-size: 50px;
  color: ${({ theme }) => theme.colors.primary};
`;

export default Home;
