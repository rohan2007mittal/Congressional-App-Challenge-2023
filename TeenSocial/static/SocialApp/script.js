let adp_underlay = document.createElement('div');
adp_underlay.className = 'adp-underlay';
document.body.appendChild(adp_underlay);
let adp = document.createElement('div');
adp.className = 'adp';
adp.innerHTML = `
    <h3>Daily Survey!</h3>
    <p style="font-style: italic;">We use this to measure your progress and give you a chance to self-reflect!</p>
    <form method="post" action="` + URL + `"> 
        ` + TOKEN + L_MOOD + `    
        <select name="mood" id="id_mood">
            <option value="1">Angry 😡</option>
            <option value="2">Anxious 😟</option>
            <option selected value="3">Neutral 😐</option>
            <option value="4">Happy 🙂</option>
            <option value="5">Excited 🤩</option>
        </select> <br><br>
        
        ` + L_TODAY + `
        <br><div class="form-check form-check-inline">
            <input required class="form-check-input" type="radio" name="today" id="id_today" value="no">
            <label class="form-check-label" for="id_today">No</label>
        </div>
        <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="today" id="id_today" value="yes">
            <label class="form-check-label" for="id_today">Yes</label>
        </div><br><br>
        ` + L_CRAVING + `
        <div><span style="margin-right: 20px;">Low</span><input name="craving" id="id_craving" type="range" min="1" max="10" value="5" style="width: 500px;"><span style="margin-left: 5px; margin-right: 20px;" id="rangeValue">5</span><span>High</span></div><br>
        ` + L_MOTIVATION + ` 
        <div><span style="margin-right: 20px;">Low</span><input name="motivation" id="id_motivation" type="range" min="1" max="10" value="5" style="width: 500px;"><span style="margin-left: 5px; margin-right: 20px;" id="rangeValue2">5</span><span>High</span></div><br> 
        ` + L_LOG + LOG + `
        <br>
        <input class="btn btn-primary" id="popupSubmit" type="submit" value="Save">  
    </form> 
`;
// <input type="number" name="craving" class="form-control" style="padding: 10px;" min="1" max="10" step="1" required="" id="id_craving">
   
document.body.appendChild(adp);
// create emoji choices for mood but have it correspond to text in forms.py (make it a choicefield)
document.getElementById('id_craving').addEventListener('change',function() {
    document.getElementById("rangeValue").innerHTML = this.value;
});
document.getElementById('id_motivation').addEventListener('change',function() {
    document.getElementById("rangeValue2").innerHTML = this.value;
});

// adp.getElementById('popupSubmit').onclick = e => {
//     e.preventDefault();
//     document.body.removeChild(adp_underlay);
//     document.body.removeChild(adp);
// };
