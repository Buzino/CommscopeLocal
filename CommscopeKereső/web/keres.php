<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kereső</title>
    <style>
        td, th {
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <script>
        tulajdonsagok = []
        muveletek = ["=", ">", "<", ">=", "<=", "tartalmazza"]
    </script>
    <?php 
    $conn = new mysqli("localhost","root","","commscopelocal");

    if ($conn->connect_error) echo "baj :c";

    $sql = "SELECT megnevezes FROM tulajdonsagok ORDER BY megnevezes ASC";
    $result = $conn->query($sql);

    if ($result->num_rows == 0) { echo "nothing here."; }
    else {
        while($row = $result->fetch_assoc()) {
            foreach ($row as $x) {
                echo "<script>tulajdonsagok.push(\"$x\")</script>";
            }
        }
    }
    ?>
    <h1>Szűrők</h1>
    <form action="<?=$_SERVER["PHP_SELF"]?>" method="post">
        <div id="szurok"></div>
        <button type="button" onclick="ujFeltetel()">Új feltétel</button>
        <button type="submit">Szűr</button>
        <input type="hidden" name="db" value=0>
    </form>
    <h1>Találatok</h1>
    <?php
    //$sql = "SELECT cikkszam, ('a'+cikkszam+'a') AS b, megnevezes, ertek, ertek2, mertekegyseg FROM specifikaciok INNER JOIN tulajdonsagok ON specifikaciok.tulajdonsag = tulajdonsagok.azon ORDER BY cikkszam, kategoria, megnevezes ASC;";
    //$sql = "SELECT cikkszam, orszag, varos, mennyiseg, mertekegyseg, lekerve FROM keszlet INNER JOIN raktarak ON keszlet.raktar = raktarak.azon ORDER BY cikkszam, lekerve";
    //$sql = "SELECT DISTINCT specifikaciok.cikkszam AS c1, keszlet.cikkszam AS c2, raktarak.orszag, raktarak.varos, keszlet.mennyiseg, keszlet.mertekegyseg FROM specifikaciok, (keszlet INNER JOIN raktarak ON keszlet.raktar = raktarak.azon) WHERE keszlet.cikkszam LIKE Concat('%',CONVERT(specifikaciok.cikkszam,VARCHAR(255)),'%') ORDER BY c1, c2, orszag ASC;";
    $sql = "SELECT cikkszam, megnevezes, ertek FROM specifikaciok INNER JOIN tulajdonsagok ON specifikaciok.tulajdonsag = tulajdonsagok.azon WHERE megnevezes LIKE 'Product Name'";
    $tul = array();
    if (isset($_POST["db"]) && (intval($_POST["db"] ?? 0) != 0)) {    
        //$sql = "SELECT cikkszam, megnevezes, ertek FROM specifikaciok INNER JOIN tulajdonsagok ON specifikaciok.tulajdonsag = tulajdonsagok.azon WHERE ";
        $sql = "SELECT cikkszam";
        $where = "HAVING 1 ";
        for ($i = 1; $i <= intval($_POST["db"]); $i++) {
            $sql .= ", (CASE WHEN megnevezes LIKE '".$_POST["tulajdonsag_$i"]."' THEN ertek END) AS `felt_$i` ";
            if ($_POST["muvelet_$i"] == "tartalmazza") {
                $muv = "LIKE";
                $where .= "AND `felt_$i` $muv '%".$_POST["ertek_$i"]."%' ";
            }else{
                $muv = $_POST["muvelet_$i"];
                $where .= "AND `felt_$i` $muv '".$_POST["ertek_$i"]."' ";
            }
            $tul[] = $_POST["tulajdonsag_$i"];
        }
        $sql .= "FROM specifikaciok INNER JOIN tulajdonsagok ON specifikaciok.tulajdonsag = tulajdonsagok.azon $where";
        echo $sql;
    }
    
    $result = $conn->query($sql);
    
    if ($result->num_rows == 0) { echo "nothing here."; }
    else {
        echo "<table>";
        echo "<tr>";
        echo "<th>Cikkszám</th>";
        foreach($tul as $t) { echo "<th>$t</th>";}
        echo "</tr>";
        while($row = $result->fetch_assoc()) {
            echo "<tr>";
            foreach($row as $x) {
                if (is_numeric(str_replace(",","",$x))) {
                    echo "<td style='max-width: 500px; text-align: right; font-weight:bold; color:red'>$x</td>";
                } else {
                    echo "<td style='max-width: 500px;'>$x</td>";
                }
            }
            echo "</tr>";
        }
        echo "</table>";
    }
?>
<script>
    function ujFeltetel() {
        szurodiv = document.getElementById("szurok");
        const sorszam = szurodiv.getElementsByClassName("feltetel").length + 1;

        lenyilo = document.createElement("select")
        lenyilo.classList.add("tulajdonsag")
        lenyilo.name = "tulajdonsag_" + (sorszam)

        tulajdonsagok.forEach((element) => {
            o = document.createElement("option")
            o.textContent = element
            lenyilo.appendChild(o)
        })
        
        muvelet = document.createElement("select")
        muvelet.classList.add("muvelet")
        muvelet.name = "muvelet_" + (sorszam)

        muveletek.forEach((element) => {
            o = document.createElement("option")
            o.textContent = element
            muvelet.appendChild(o)
        })

        szoveg = document.createElement("input")
        szoveg.classList.add("ertek")
        szoveg.name = "ertek_" + (sorszam)
        szoveg.type = "text"

        torol = document.createElement("button")
        torol.textContent = "Töröl"
        torol.name = "torol_"+sorszam;
        torol.onclick = (event) => torolFeltetel(sorszam)
        
        ujdiv = document.createElement("div")
        ujdiv.classList.add("feltetel")
        ujdiv.id = "feltetel_" + (sorszam)

        ujdiv.appendChild(lenyilo)
        ujdiv.appendChild(muvelet)
        ujdiv.appendChild(szoveg)
        ujdiv.appendChild(torol)
        szurodiv.appendChild(ujdiv)

        document.querySelector("input[name='db']").value++;
    }

    function torolFeltetel(sorszam) {
        document.querySelector("div#feltetel_"+sorszam).remove();
        document.querySelector("input[name='db']").value--;
    }
</script>
</body>
</html>