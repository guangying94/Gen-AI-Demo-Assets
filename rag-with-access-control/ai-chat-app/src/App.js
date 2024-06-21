import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { getUserInfo } from './services';
import { useEffect, useState } from "react";
import LLMChatApp from './chatInterface';


function App() {

  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    async function fetchUserInfo() {
      const info = await getUserInfo();
      setUserInfo(info);
    }

    fetchUserInfo();
  }, []);

  return (
    <>
      <Box sx={{ bgcolor: '#cfe8fc', height: '5vh' }}>
        <Container>
          <Stack direction="row" spacing={2} alignItems="center" justifyContent="space-between" height={'5vh'}>
            <h2>RAG With Access Control</h2>
            {userInfo ?
              <>
                <Button
                  variant="contained"
                  href="/.auth/logout"
                  color='error'
                >
                  Sign Out
                </Button>
              </> :
              <>
                <Button
                  variant="contained"
                  href="/.auth/login/aad"
                >
                  Sign In
                </Button>
              </>}
          </Stack>
        </Container>
      </Box>
      <Container>
          {
            userInfo ?
            <Stack spacing={2} alignItems="center" justifyContent="center" p={'1rem'}>
                <h2>Welcome {userInfo.userDetails}!</h2>
                <p>Your current role(s): {userInfo.userRoles.join(', ')}</p>

                <LLMChatApp userInfo={userInfo}/>




              </Stack>
              :
              <Stack spacing={2} alignItems="center" justifyContent="center" p={'1rem'}>
                <h2>Welcome Guest!</h2>
                <p>Please sign in to access the app!</p>
                <Button
                  variant="contained"
                  href="/.auth/login/aad"
                >
                  Sign In
                </Button>
              </Stack>
          }
      </Container>
    </>
  );
}

export default App;
