import React, { useState, useRef, useEffect } from 'react';
import Draggable from 'react-draggable';

import './App.css';
import dvd from './assets/dvd.png'
import dvd_open from './assets/dvd_open.png'
import remote from './assets/remote.png'
import laugh_track from './assets/laugh.mp3'
import disk_drive from './assets/disk_drive.mp3'
import useSound from 'use-sound';

import { createFFmpeg, fetchFile } from '@ffmpeg/ffmpeg';
const ffmpeg = createFFmpeg({ log: true });

function App() {
  const [ready, setReady] = useState(false);
  const [video, setVideo] = useState();
  const [audio, setAudio] = useState();
  const [data, setData] = useState({});

  const [play] = useSound(disk_drive);

  const hiddenInput = useRef(null);

  const load = async () => {
    await ffmpeg.load();
    setReady(true);
  }

  useEffect(() => {
    const laugh = new Request(laugh_track);

    fetch(laugh).then((response) => response.blob())
    .then((myBlob) => {
      const objectURL = URL.createObjectURL(myBlob);
      setAudio(objectURL)
    })
    load();
  }, [])

  const open = (e) => {
    e.currentTarget.src=dvd_open;
    play();
  }

  const close = (e) => {
    e.currentTarget.src=dvd;
    play();
  }

  const upload = async (e) => {
    // Write the file to memory 
    ffmpeg.FS('writeFile', 'joke.mp4', await fetchFile(e.target.files?.item(0)));
    ffmpeg.FS('writeFile', 'funny.mp3', await fetchFile(audio));

    // Run the FFMpeg command
    //await ffmpeg.run('-i','joke.mp4','-i','laugh.mp3','-filter_complex','[1:a]adelay=16000|16000[laugh];[0:a][laugh]amix=inputs=2:duration=longest[audio_out]','-map','0:v','-map','[audio_out]','-y','output.mp4');

    // await ffmpeg.run('-i','joke.mp4','-vn','-y','output.wav');
    // await ffmpeg.run('-i','joke.mp4', 'output.mp3');

    // Read the result

    
    // var data = new FormData();
    // data.append('somethingelse', file, 'somethingelse');

    const data = await fetch('http://localhost:5000/receive', {
          method: 'POST',
          body: e.target.files?.item(0),
      }).then(res => res.json());
    await ffmpeg.run('-i','joke.mp4','-i',`${data.data[1]}.mp3`,'-filter_complex',`[1:a]adelay=${data.data[0]}|${data.data[0]}[track];[0:a][track]amix=inputs=2:duration=longest[audio_out]`,'-map','0:v','-map','[audio_out]','-y','output.mp4');
    const buffer = ffmpeg.FS('readFile', 'output.mp4');

    const blob = new Blob([buffer.buffer], {type: "video/mp4"});
    setVideo(blob);
    // console.log(audioData)
    // Create a URL
    //const blob = new  Blob([data.buffer], {type: "video/mp4"});
    //setVideo(blob);
  }

  return ready ? (
    
    <div className="App">
      { video && <video
        className='Video'
        controls
        width="41%"
        src={URL.createObjectURL(video)}>

      </video>}

      <button className='Upload' onClick={() => hiddenInput.current.click()}>
          <img
            onMouseOver={(e) => open(e)}
            onMouseOut={(e) => close(e)}
            src={dvd} alt="" border="0" width="73%"></img>
      </button>

      <input type="file" accept='.mp4' style={{display:'none'}} ref={hiddenInput} onChange={(e) => upload(e)} />
      <Draggable bounds="parent">
        <div className='Remote'>
          <img src={remote} alt="" border="0" height="100%"></img>
          <button className='Tags'></button>
          <button className='Up'></button>
          <button className='Down'></button>
        </div>
      </Draggable>
    </div>
  )
    :
    (
      <p>Loading...</p>
    );
}

export default App;