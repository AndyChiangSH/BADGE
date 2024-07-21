$(function () {
    init();

    function init() {
        $('#data').show();
        $('#report').hide();
        $('#score').hide();
        $('#generate').show();
        $('#generating').hide();
        $('.data_select').change(generate_prompt);
        generate_prompt();
        $('#evaluate').show();
        $('#evaluating').hide();
    }

    function generate_prompt() {
        let game = $("#game").val();
        let input_data_type = $("#input_data_type").val();
        let in_context_learning = $("#in_context_learning").val();
        let large_language_models = $("#large_language_models").val();

        // console.log(game, input_data_type, in_context_learning, large_language_models);

        let prompt_path = "../prompt/generation/" + input_data_type + "+" + in_context_learning + ".txt"
        $.get(prompt_path, function (prompt) {
            let data_path = "../" + input_data_type + "/" + game + "/" + input_data_type + ".txt";
            $.get(data_path, function (data) {
                prompt = prompt.replace("{" + input_data_type + "}", data)
                // console.log("prompt:", prompt);
                $('#generate_prompt_text').text(prompt);
            });
        });
    }

    $('#generate').click(generate);

    function generate() {
        $('#data').show();
        $('#report').hide();
        $('#score').hide();
        $('#generate').hide();
        $('#generating').show();

        setTimeout(function () {
            $('#data').show();
            $('#report').show();
            $('#score').hide();
            $('#generate').show();
            $('#generating').hide();
    
            let game = $("#game").val();
            let input_data_type = $("#input_data_type").val();
            let in_context_learning = $("#in_context_learning").val();
            let large_language_models = $("#large_language_models").val();
    
            let report_path = "../generation/" + game + "/" + large_language_models + "/" + input_data_type + "+" + in_context_learning + ".txt"
            // console.log("report_path:", report_path);
            $.get(report_path, function (report) {
                // console.log("report:", report);
                $('#report_text').text(report);
                $('.report_select').change(evaluate_prompt);
                evaluate_prompt();
            });
        }, 1000 + get_random_int(0, 1000));
    }

    function evaluate_prompt() {
        let evaluation_criteria = $("#evaluation_criteria").val();
        let report = $('#report_text').text();

        // console.log(evaluation_criteria, report);

        let prompt_path = "../prompt/evaluation/" + evaluation_criteria + ".txt";
        $.get(prompt_path, function (prompt) {
            prompt = prompt.replace("{Badminton Report}", report)
            // console.log("prompt:", prompt);
            $('#evaluate_prompt_text').text(prompt);
        });
    }

    $('#evaluate').click(evaluate);

    function evaluate() {
        $('#data').show();
        $('#report').show();
        $('#score').hide();
        $('#evaluate').hide();
        $('#evaluating').show();

        setTimeout(function () {
            $('#data').show();
            $('#report').show();
            $('#score').show();
            $('#evaluate').show();
            $('#evaluating').hide();

            let game = $("#game").val();
            let input_data_type = $("#input_data_type").val();
            let in_context_learning = $("#in_context_learning").val();
            let large_language_models = $("#large_language_models").val();
            let evaluation_criteria = $("#evaluation_criteria").val();

            let score_path = "../evaluation/" + game + "/" + large_language_models + "/" + input_data_type + "+" + in_context_learning + ".txt/" + evaluation_criteria + ".txt"
            // console.log("score_path:", score_path);
            $.get(score_path, function (score) {
                // console.log("score:", score);
                $('#score_text').text(score);
            });
        }, 1000 + get_random_int(0, 1000));
    }

    $("#copy_report").click(function () {
        let report = $('#report_text').text();
        navigator.clipboard.writeText(report).then(function () {
            alert("Copy to clipboard successful.");
        }, function (err) {
            alert("Copy to clipboard fail!");
        });
    })

    $("#download_report").click(function () {
        let report = $('#report_text').text();
        this.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
        this.setAttribute('download', "report.txt");
    })

    $("#copy_score").click(function () {
        let score = $('#score_text').text();
        navigator.clipboard.writeText(score).then(function () {
            alert("Copy to clipboard successful.");
        }, function (err) {
            alert("Copy to clipboard fail!");
        });
    })

    $("#download_score").click(function () {
        let score = $('#score_text').text();
        this.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(score));
        this.setAttribute('download', "score.txt");
    })

    function get_random_int(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
});
