import { useState, useEffect } from "react";

class Circle {
    constructor(ctx, canvas, x, y, jitter) {
        this.ctx = ctx;
        this.canvas = canvas;
        this.x = x;
        this.y = y;
        this.size = jitter;
        this.opacity = 1;

        this.draw = function () {
            this.ctx.strokeStyle = `rgba(255, 255, 255, 255)`;
            this.ctx.beginPath();
            this.ctx.arc(this.x + Math.random()*10-5, this.y + Math.random()*10-5, this.size * this.opacity, 0, Math.PI * 2);
            this.ctx.stroke();
        };

        this.update = function () {
            this.opacity -= 0.005 * Math.random();
            if (this.opacity <= 0) {
                this.reset();
            }
        };

        this.reset = function () {
            this.x = Math.random() * this.canvas.width;
            this.y = Math.random() * this.canvas.height;
            this.opacity = 1;
        };
    }
}

function Transition(props) {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const canvas = document.getElementById('transition');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // 전기 배열 생성
        const circles = [];
        for (let i = 0; i < 10; i++) {
            const x = 0.5 * canvas.width;
            const y = 0.5 * canvas.height;
            let size = canvas.width*0.2;
            size = size + size * 0.1 * Math.random();
            circles.push(new Circle(ctx, canvas, x, y, size));
        }

        // 애니메이션 프레임
        function animate() {
            // 화면 초기화
            ctx.fillStyle = `rgba(0, 0, 0, 0.1)`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 전기 그리기 및 업데이트
            for (let i = 0; i < circles.length; i++) {
                circles[i].draw();
                circles[i].update();
            }

            //draw text
            ctx.font = "30px Arial";
            ctx.fillStyle = "white";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            
            let percent = props.count > count ? (100*count/props.count) : 100; 
            ctx.fillText(`${percent.toFixed(2)}%`, canvas.width/2, canvas.height/2);
            // 애니메이션 반복 실행
            //requestAnimationFrame(animate);
        }

        // 애니메이션 시작
        animate();
    }, [count, props.count]);

    useEffect(() => {
        if(count >= props.count*1.5){
            props.setStatus(true);
        }
        setTimeout(() => {
            setCount(count + 0.01);
        }, 0);
    }, [props, count]);

    return <div className="container">
            <canvas id="transition" className="element" 
                style={{width : "50vw", height : "50vh"}}></canvas>
    </div>
}
export default Transition;