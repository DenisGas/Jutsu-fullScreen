// ==UserScript==
// @name         Jutsu AutoFulscreen
// @namespace    http://tampermonkey.net/
// @version      2023-12-04
// @description  autofullscreen with tray app
// @author       DenisGasilo
// @match        https://jut.su/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=jut.su
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

     const page = window.location.href;

    function goFullScreen() {
        const fullScreenControl = document.querySelector(
            ".vjs-fullscreen-control"
        );
        fullScreenControl.click();
    }

    function kino(){
        document.querySelector("html").style.cssText = 'overflow-y: hidden;';
        document.querySelector(".main.wrapper.z_fix").style.cssText = 'max-width: 100%; border: 0px';
        document.querySelector(".content").style.width = "100%";
        document.querySelector(".border_around_video").style.maxWidth = "100%";
        document.querySelector(".sidebar").style.display = "none";
        document.querySelector(".slicknav_menu").style.display = "none";
        document.querySelector(".header").style.display = "none";
        document.querySelector(".logo_b ").style.display = "none";
        document.querySelector(".info_panel").style.display = "none";
        document.querySelector(".achiv_switcher").style.display = "none";
        document.querySelector(".video_plate_title").style.display = "none";
        document.querySelector(".header_video").style.display = "none";
        document.querySelector(".all_anime_title.aat_ep").style.display = "none";
    }

    function workOnThisPage(websitePage) {
        if (websitePage.includes("episode-") || websitePage.includes("film-")) {
            return true;
        }
        return false;
    }

     if (workOnThisPage(page) != false) {

     const socket = new WebSocket('ws://localhost:8765');

    socket.addEventListener('open', (event) => {
        //console.log('WebSocket connection is open:', event);
    });

    socket.addEventListener('message', (event) => {
       console.log('Received message from server:', event.data);
    });

    socket.addEventListener('close', (event) => {
        if (event.wasClean) {
            //console.log(`Connection lost clean code: ${event.code}, cause: ${event.reason}`);
        } else {
            //console.error('Connection lost');
        }
    });

    socket.addEventListener('error', (event) => {
        //console.error('Error:', event);
    });




        const GetVideoI = setInterval(() => {
        const video = document.getElementById("my-player_html5_api");
        if (video) {
          clearInterval(GetVideoI);
          const getFCntlI = setInterval(() => {
            if (document.querySelector(".vjs-fullscreen-control") && video.paused === false) {
              clearInterval(getFCntlI);
              document.querySelector(".vjs-fullscreen-control").addEventListener('click', () => video.focus());
                socket.send("fullscreen")

              document.addEventListener('keydown', function (event) {
                if (event.code === "KeyF") {
                  const message = document.querySelector('#message');
                  const search = document.querySelector('input[type="text"][name="ystext"]');
                  if (message !== document.activeElement && search !== document.activeElement) {
                    goFullScreen();
                  }

                }
              });
            }
          }, 100);
          }
        }
      , 100);
     }


})();