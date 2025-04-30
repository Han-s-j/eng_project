<section id="title">
            <div id="title_name">👄</div>
            <hr>
         </section>
         <section id="user_box">
            <div id="user_sent">
            <h2>🗣️ 연습 문장</h2>
                " ${userSent.mySent} "
            </div>
            <div id="audio_box">
            	<audio id="ttsAudio" controls></audio>
            </div>
            <div id="chart_box">
	            <div id="loading" style="position: absolute;
	            	top: 50%;
	            	left: 50%;
	            	transform: translate(-50%, -50%);
	            	font-weight: bold;
	            	font-size: 18px;
	            	display: none;
	            	">
	            	<img src="/resources/assets/img/loading.gif">
	            	생성 중...
	            </div>
            	<h3>📈 강세 분석</h3>
            	<canvas id="stressChart" width="800" height="400"></canvas>
            </div>
         </section>
	</div>
